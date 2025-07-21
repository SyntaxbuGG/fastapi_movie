# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    PROJECT_NAME: str = "Moviestra"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int =  7
 
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    EMAIL_FROM: str = "noreply@example.com"
    BASE_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Кэшируем — вызывается один раз при старте
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
