import os

from typing import Any
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv('./configs/.env')


class Settings(BaseSettings):
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_PORT = os.getenv("DB_PORT")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

    ETH_PROVIDER = os.getenv("ETH_PROVIDER")

    ETH_PUBLIC_KEY = os.getenv("ETH_PUBLIC_KEY")
    ETH_PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY")

    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
    CONTRACT_ABI = os.getenv("CONTRACT_ABI")


settings: Settings = Settings()
