from datetime import timedelta
from datetime import datetime as dt
import hashlib
import jwt
import uuid

import smtplib
import ssl
import traceback
import sys
from string import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_an_email(receiver_email:str, subject:str, template:str, variables:dict):
    # User configuration
    sender_email = 'noreply@daily-meditation.app'
    password = 'k1ng@rthur'

    # Email text
    email_template = Template(template)
    TEXT = email_template.substitute(variables) if variables else template

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    # Create the plain-text and HTML version of your message
    text = TEXT
    html = f"<html><body>{TEXT}</body></html>"

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)


    # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
    server = smtplib.SMTP('smtp.office365.com', 587)
    # Encrypts the email
    context = ssl.create_default_context()
    server.starttls(context=context)

    # We log in into our Google account
    server.login(sender_email, password)
    # Sending email from sender, to receiver with the email body
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def reset_email(receiver_email:str, subject:str, variables:dict):
    
    email = [receiver_email]
    title = subject
    user_info = variables

    template = """
    <p>Hello $name,</p>
    <p>We recieved a request to reset your password. To reset your password, please click the link below:</p>
    <a href='$url'>$url</a>


    """
    send_an_email(email, title, template, user_info)


def create_token(
    content: dict,
    days_until_expiration: float = None,
    key: str = "b58831ce-ecb7-403d-b75e-2ab24d945cf7",
    algorithm="HS256",
) -> str:
    """Generate a JSON Web Token (JWT) with specified content payload."""
    if days_until_expiration is not None:
        content["exp"] = dt.now() + timedelta(days=days_until_expiration)
    # return jwt.encode(content, key, algorithm=algorithm)
    return str(jwt.encode(content, key, algorithm=algorithm).decode("UTF-8"))


def verify_token(token, key: str = "b58831ce-ecb7-403d-b75e-2ab24d945cf7") -> dict:
    """Verify the validity of a JSON Web Token."""
    try:  # to decode the JWT
        content = jwt.decode(token, key)
        content["errors"] = ""
        return True, content
    except Exception as e:  # oops — report reason for error
        return False, {"errors": e.args[0]}


def hash_password(password: str) -> str:
    """Hash the password using a randomly generated salt and SHA256 hashing."""
    salt = uuid.uuid4().hex
    # Returns the hash : salt, so we can check passwords later.
    return hashlib.sha512(salt.encode() + password.encode()).hexdigest() + ":" + salt


def check_password(hashed_password: str, user_password: str) -> bool:
    """Verify that user password matches the existing hashed password."""
    password, salt = hashed_password.split(":")
    return (
        password == hashlib.sha512(salt.encode() + user_password.encode()).hexdigest()
    )
