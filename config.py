import os
from dataclasses import dataclass
from typing import TypedDict

from dotenv import load_dotenv
from pathlib import Path


PROJECT_DIR = Path(__file__).parent
load_dotenv(Path(PROJECT_DIR, ".env"))


@dataclass(frozen=True)
class Config(TypedDict):
    pass


@dataclass(frozen=True)
class PGSettings:
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = int(os.environ.get("DB_PORT"))
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_NAME: str = os.environ.get("DB_NAME")