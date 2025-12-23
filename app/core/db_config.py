from dotenv import load_dotenv
import os
import psycopg2
import psycopg2.extensions

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


def connect_to_db() -> psycopg2.extensions.connection:
    """Return a new psycopg2 connection using environment variables."""
    try:
        dsn = (
            f"dbname={DB_NAME} "
            f"user={DB_USER} "
            f"password={DB_PASSWORD} "
            f"host={DB_HOST} "
            f"port={DB_PORT}"
        )
        return psycopg2.connect(dsn=dsn)
    except Exception as exc:
        raise RuntimeError(f"Failed to connect to database: {exc}") from exc
