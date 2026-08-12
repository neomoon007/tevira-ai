from sqlalchemy import text

from src.tevira_ai.db.database import engine


def check_db_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            db_version = result.fetchone()

            print("Database connection is working!")
            print(f"Postgresql version: {db_version}")

    except Exception as exception:
        print("Database connection is NOT working!")
        print(f"Error details: {exception}")


check_db_health()
