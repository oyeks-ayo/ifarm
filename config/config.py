import os
from dotenv import load_dotenv

load_dotenv()

class Appconfig(object):
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')

# export PATH=$PATH:"/c/Program Files/PostgreSQL/18/bin" TO ADD POSTGRESQL TO PATH ON WINDOWS
# $ psql -U postgres TO ACCESS POSTGRESQL TERMINAL
# CREATE DATABASE ifarm_db; TO CREATE DATABASE IN POSTGRESQL TERMINAL