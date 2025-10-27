from pathlib import Path
from typing import Union

from dotenv import dotenv_values
from sqlalchemy import engine, URL
from sqlmodel import create_engine


def get_engine(dotenv_path: Union[Path, str]) -> engine.Engine:
    config = dotenv_values(dotenv_path)
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
    return create_engine(db_url, echo=DEBUG, connect_args=connect_args)
