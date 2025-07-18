from pydantic_settings import BaseSettings

import os

class Settings(BaseSettings):
    # GOOGLE_CLIENT_ID: str
    # GOOGLE_CLIENT_SECRET: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")

settings = Settings()
