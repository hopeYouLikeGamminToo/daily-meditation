import config
from models.user import User, SignUpRequest
from models.database import verify_input, query
from tools import hash_password, create_token, verify_token, check_password

import jwt
import uuid
import hashlib
import requests

from typing import Union
from datetime import datetime, timedelta
from fastapi import Header, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2AuthorizationCodeBearer

router = APIRouter()

# Initialize OAuth2
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="https://oauth2.googleapis.com/token",
    authorizationUrl="https://accounts.google.com/o/oauth2/auth"
    )

def hash_password(password: str) -> str:
    #Hash the password using a randomly generated salt and SHA256 hashing.
    salt = uuid.uuid4().hex
    # Returns the hash : salt, so we can check passwords later.
    return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt

def create_token(content: dict, days_until_expiration: float = None, key: str = "b58831ce-ecb7-403d-b75e-2ab24d945cf7", algorithm="HS256") -> str:
    # Generate a JSON Web Token (JWT) with specified content payload.
    if days_until_expiration is not None:
        content["exp"] = datetime.now() + timedelta(days=days_until_expiration)
    return jwt.encode(content, key, algorithm=algorithm)

@router.get("/check_availability")
def check_availability(username:str)->bool:
    if not verify_input([username]):
        return False

    sql = f"""select * from users where username ilike '{username}'"""
    ret = query(sql)
    print(ret)
    if len(ret)>0:
        return False
    else:
        return True

@router.get("/get_user")
def get_user(username:str=None)->dict:
    print(f"getting {username}")

    if not verify_input([username]):
        return None

    user = User.by_username(username)
    
    # return user.json ? 

    return {    
            "user_id":user.user_id,
            "username":user.username,
            "email":user.email,
            "last_login":user.last_login,
            "created_at":user.created_at,
            "total_games_played":user.total_games_played,
            "total_wins":user.total_wins,
            "total_losses":user.total_losses,
            "win_streak":user.win_streak,
            "phone_number":user.phone_number,
            "login_type":user.login_type,
            "google_id":user.google_id,
            "last_game":user.last_game
        }

@router.post("/update_user")
def update_user(currentUsername:str=None, newUsername:str=None, email:str=None, phone_number:str=None, currentPassword:str=None, newPassword:str=None) -> dict:
    if not verify_input([currentUsername]):
        return None

    user = User.by_username(currentUsername)
    print(f"updating: {user.user_id}")
    
    if currentPassword and newPassword:
        if not check_password(user.password_hash, currentPassword):
            raise HTTPException(status_code=401, detail="Incorrect current password")
        user.password_hash = hash_password(newPassword)
        
    user.username = newUsername if (newUsername is not None and len(newUsername) >= 4) else user.username
    user.email = email if email is not None else user.email
    user.phone_number = phone_number if phone_number is not None else user.phone_number
    user.save()

    return {"status": "ok", "code": 200}

@router.post("/update_stats")
def update_stats(username:str, win:int=None) -> dict:
    user = User.by_username(username)
    
    user.total_games_played += 1
    user.last_game = datetime.now()
    
    if win:
        user.total_wins += 1
        user.win_streak += 1
    else:
        user.total_losses += 1
        user.win_streak = 0

    user.save()

    return {"status": "ok", "code": 200}

@router.post("/sign_up")
async def sign_up(login_request: SignUpRequest) -> Union[User, JSONResponse]:
    print("login_request: ", login_request)

    if check_availability(login_request.username):
        # create new user
        new_user = User()
        new_user.email = login_request.email
        new_user.username = login_request.username
        new_user.password_hash = hash_password(login_request.password)
        new_user.created_at = datetime.now()
        new_user.last_login = new_user.created_at
        new_user.login_type = login_request.login_type
        new_user.google_id = login_request.google_id
        new_user.phone_number = login_request.phone_number

        new_user.save()

        return new_user
    else:
        # check password for existing user
        existing_user = User.by_username(login_request.username)
        print(f"existing_user: {existing_user}")
        hashed_password = existing_user.password_hash
        if not check_password(hashed_password, login_request.password):
            return JSONResponse(content={"error": "Incorrect password"}, status_code=401)

        # Update last login time
        existing_user.last_login = datetime.now()
        existing_user.save()

        return existing_user


def get_google_user(token: str = Depends(oauth2_scheme)):
    # Normally, you would validate the token and fetch the user info from Google
    # For demonstration purposes, we'll just check if a token is provided.
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Here, you'd decode and validate the token and get the user's info.
    # We'll just return a mock user.
    return {"username": "JohnDoe", "token": token}

@router.post("/get_google_token")
async def get_google_token(authorization_code: str):
    data = {
        "client_id": config.CLIENT_ID,
        "client_secret": config.CLIENT_SECRET,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": "your_redirect_uri_here"  # Replace with your actual redirect URI
    }
    
    r = requests.post("https://oauth2.googleapis.com/token", data=data)
    
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Could not get token")
    
    return r.json()

@router.post("/google_login")
async def google_login(current_user: dict = Depends(get_google_user)):
    # Your login logic here. For now, we'll just return the mock user info
    return {"message": "Successfully logged in", "user": current_user}
