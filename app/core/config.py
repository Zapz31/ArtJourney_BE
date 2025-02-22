from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    DATABASE_URL: str = os.getenv("DATABASE_URL")

settings = Settings()