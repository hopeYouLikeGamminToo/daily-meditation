
from pydantic import BaseModel
from datetime import datetime

from models.database import connection, execute, query, safe_format, guid, execute_param


class SignUpRequest(BaseModel):
    email: str
    username: str
    password: str
    login_type: str = None
    google_id: str = None
    phone_number: str = None
    
class User(BaseModel):
    user_id: str = None
    username: str = None
    email: str = None
    password_hash: str = None
    last_login: datetime = None
    created_at: datetime = None
    total_games_played: int = None
    total_wins: int = None
    total_losses: int = None
    win_streak: int = None
    phone_number: str = None
    login_type: str = None
    google_id: str= None
    last_game: str= None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if len(args) > 0:
            self.user_id = args[0]
            self.username = args[1]
            self.email = args[2]
            self.password_hash = args[3]
            self.last_login = args[4]
            self.created_at = args[5]
            self.total_games_played = args[6]
            self.total_wins = args[7]
            self.total_losses = args[8]
            self.phone_number = args[9]
            self.login_type = args[10]
            self.google_id = args[11]
            self.win_streak = args[12]
            self.last_game = args[13]


    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT current_timestamp,
                total_games_played INT DEFAULT 0,
                total_wins INT DEFAULT 0,
                total_losses INT DEFAULT 0,
                phone_number VARCHAR(15) UNIQUE,
                login_type VARCHAR(50),
                google_id VARCHAR(255) UNIQUE,
                win_streak INT,
                last_game TIMESTAMP
            );
        """
        execute(sql)

    @classmethod
    def drop_table(self):
        print(f"Dropping Table")
        sql = """
            DROP TABLE users
        """
        execute(sql)

    @classmethod
    def by_username(self, username):
        sql = f"""
            SELECT * FROM users WHERE username = '{username}'
        """
        ret = query(sql)
        print(f"by_username: {ret}")
        if ret:
            return User(*ret[0])
        return None

    @classmethod
    def by_user_id(self, user_id):
        sql = f"""
            SELECT * FROM users WHERE user_id = '{user_id}'
        """
        print(sql)
        ret = query(sql)
        return User(*ret[0])

    def delete(self, cursor):
        if self.user_id is not None:
            sql = f"""
                    DELETE FROM users
                    where user_id = '{self.user_id}'
                """
            execute(sql)

    def save(self):
        print(f"user_id: {self.user_id}")

        if self.user_id is not None:
            print("updating existing user")
            sql = """
                UPDATE users SET
                username = %s,
                email = %s,
                password_hash = %s,
                last_login = %s,
                created_at = %s,
                total_games_played = %s,
                total_wins = %s,
                total_losses = %s,
                phone_number = %s,
                login_type = %s,
                google_id = %s,
                win_streak = %s,
                last_game = %s
                WHERE user_id = %s
            """
            params = (
                self.username,
                self.email,
                self.password_hash,
                self.last_login,
                self.created_at,
                self.total_games_played,
                self.total_wins,
                self.total_losses,
                self.phone_number,
                self.login_type,
                self.google_id,
                self.win_streak,
                self.last_game,
                self.user_id
            )
            execute_param(sql, params)
        else:
            print("creating new user")
            self.user_id = guid()
            sql = """
                INSERT INTO users VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """
            params = (
                self.user_id,
                self.username,
                self.email,
                self.password_hash,
                self.last_login,
                self.created_at,
                self.total_games_played,
                self.total_wins,
                self.total_losses,
                self.phone_number,
                self.login_type,
                self.google_id,
                self.win_streak,
                self.last_game
            )
            execute_param(sql, params)


