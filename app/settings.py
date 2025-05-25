import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")
ACCESS_TOKEN_TTL = int(os.getenv("ACCESS_TOKEN_TTL"))
SECRET_KEY = os.getenv("SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
