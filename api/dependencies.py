# api/dependencies.py
from typing import Generator
from app.db.session import db_session


def get_db() -> Generator:
    """Dependency for getting database session in route handlers."""
    session = db_session.get_session()
    try:
        yield session
    finally:
        session.close()
