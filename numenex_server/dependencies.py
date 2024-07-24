import logging
from .database import Database
from fastapi import Request


logger = logging.getLogger(__name__)


class DatabaseDependency:
    def __init__(self, db: Database) -> None:
        self.db = db

    def __call__(self, request: Request) -> None:
        request.state.db = self.db


def get_session(request: Request):
    yield from request.state.db.get_session()
