import pytest


@pytest.fixture
def test_client():
    from src.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture(scope="session")
def database():
    from src.db.database import get_db
    db = next(get_db())
    yield db


@pytest.fixture(autouse=True)
def clean_database(database):
    yield

    from sqlalchemy.exc import SQLAlchemyError
    from src.db import models
    try:
        database.query(models.Friendship).delete()
        database.commit()
    except SQLAlchemyError:
        database.rollback()


@pytest.fixture(autouse=True)
def clean_cache():
    yield
    from src.cache import redis_cache
    redis_cache.delete_all()
