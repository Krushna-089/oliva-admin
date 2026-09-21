import os

from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_NAME = os.getenv("DB_NAME", "oliva_scm")

    SQLALCHEMY_DATABASE_URI = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        query={"charset": "utf8mb4"},
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
