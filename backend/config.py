import os
from dotenv import load_dotenv

# load environmental variables
load_dotenv()

# Read Google OAuth2 credentials
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# zbox postgres database server connection
HOST = '10.0.0.117'
PORT = 5432
USER = 'matthew'
PASSWORD = 'k1ng@rthur'
DBNAME = 'daily_meditation'