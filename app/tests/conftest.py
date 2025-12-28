import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models.base import Base
import os
from dotenv import load_dotenv
load_dotenv()

TEST_DB_URL =  os.getenv("POSTGRES_URL")


@pytest.fixture
def session():
    engine = create_engine(TEST_DB_URL)

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(engine)
