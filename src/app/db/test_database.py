import os

from dotenv import load_dotenv

from src.app.db.database import create_session

load_dotenv()

TEST_DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}"
    f"@localhost:5432/"
    f"{os.getenv('POSTGRES_TEST_DB')}"
)

engine, SessionLocal = create_session(TEST_DATABASE_URL)
