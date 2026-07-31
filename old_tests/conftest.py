import pytest
from fastapi.testclient import TestClient

from src.app.db.test_database import SessionLocal
from src.app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    session = SessionLocal()

    yield session

    session.rollback()
    session.close()
