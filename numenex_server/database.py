from contextlib import contextmanager

from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

__all__ = ["DatabaseConfig", "Database"]


class DatabaseConfig(BaseModel):
    connection_string: str


class Database:
    engine: Engine
    config: DatabaseConfig

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.create_database_engine()

    def create_database_engine(self):
        self.engine = create_engine(self.config.connection_string, pool_size=8)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        with self.sessionmaker() as sess:
            yield sess

    @contextmanager
    def get_session_ctx(self):
        yield from self.get_session()
