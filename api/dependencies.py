from pathlib import Path

from sqlmodel import SQLModel, Session

from db.engine import get_engine

BASE_DIR = Path(__file__).resolve().parent.parent
#DOTENV_PATH = BASE_DIR / "db" / ".env.dev"
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
