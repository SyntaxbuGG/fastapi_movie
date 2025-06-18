import os
from sqlmodel import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
from passlib.context import CryptContext


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()  # Загружаем переменные из .env


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    bind=engine, class_=Session, autoflush=False, autocommit=False
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
