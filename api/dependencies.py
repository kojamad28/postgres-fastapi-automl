from dotenv import dotenv_values
from sqlalchemy import URL
from sqlmodel import SQLModel, Session, create_engine


#config = dotenv_values("db/.env.dev")
config = dotenv_values("db/.env")


DEBUG = config.get("DEBUG", "false").lower() == "true"


db_url = URL.create(
        "postgresql+psycopg",
        username=config["POSTGRES_USER"],
        password=config["POSTGRES_PASSWORD"],  # plain (unescaped) text
        host=config.get("POSTGRES_HOST", "postgres"),
        port=config.get("POSTGRES_PORT", "5432"),
        database=config.get("POSTGRES_DB", "postgres"),
        query={"options": f"-c search_path={config.get('POSTGRES_SCHEMA', 'public')}"},
)
connect_args = {}
engine = create_engine(db_url, echo=DEBUG, connect_args=connect_args)


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
