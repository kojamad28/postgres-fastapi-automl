import os
from pathlib import Path

from sqlmodel import SQLModel, Session

from db.engine import get_engine


def read_boolean(value: str) -> bool:
    return value.lower() in ("true", "t", "yes", "y", "on", "1")

DEBUG = read_boolean(str(os.environ.get("DEBUG", "False")))

BASE_DIR = Path(__file__).resolve().parent.parent

if DEBUG:
    DOTENV_PATH = BASE_DIR / "db" / ".env.dev"
else:
    DOTENV_PATH = BASE_DIR / "db" / ".env"

engine = get_engine(DOTENV_PATH)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def get_session():
    session = Session(engine)
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
