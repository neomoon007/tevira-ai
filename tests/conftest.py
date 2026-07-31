import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.app.db.test_database import engine
from src.app.main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def db_session():
    connection = engine.connect()

    transaction = connection.begin()

    TestSession = sessionmaker(
        bind=connection, join_transaction_mode="create_savepoint"
    )

    session = TestSession()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
