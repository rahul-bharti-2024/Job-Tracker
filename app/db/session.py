
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from typing import Optional, Generator
from urllib.parse import quote_plus
import logging

load_dotenv()

# -------------------------------------------------
# Globals (initialized explicitly)
# -------------------------------------------------
engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None


# -------------------------------------------------
# Initialization
# -------------------------------------------------
def init_engine(database_url: str) -> None:
    """
    Initialize SQLAlchemy engine + sessionmaker.
    Must be called exactly once at startup.
    """
    global engine, SessionLocal

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        future=True,
    )

    # expire_on_commit=False keeps objects usable after commit
    SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )


# -------------------------------------------------
# Dependency
# -------------------------------------------------
def get_session() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy `Session` for use as a dependency.

    Commits after the `yield`. Rolls back on exception and always closes.
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_engine() first.")

    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        logging.exception("Session rollback due to exception")
        db.rollback()
        raise
    finally:
        db.close()


# -------------------------------------------------
# Helper (production only)
# -------------------------------------------------
def build_postgres_url() -> str:
    """Build a safe Postgres URL from environment variables.

    If `DATABASE_URL` is set it will be returned verbatim (useful for tests/CI).
    Username and password are URL-encoded to handle special characters.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
        raise ValueError("POSTGRES_USER, POSTGRES_PASSWORD and POSTGRES_DB must be set")

    user_q = quote_plus(POSTGRES_USER)
    pwd_q = quote_plus(POSTGRES_PASSWORD)

    return f"postgresql+psycopg2://{user_q}:{pwd_q}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def dispose_engine() -> None:
    """Dispose the engine and reset module globals.

    Useful for clean shutdown and test isolation.
    """
    global engine, SessionLocal
    if engine is not None:
        try:
            engine.dispose()
        finally:
            engine = None
            SessionLocal = None
