# app/db/init_db.py
from .session import engine
from .base import Base
from app.models import user, status, source, tag, application, update  # import all models

def init_db():
    Base.metadata.create_all(bind=engine)

# SQLAlchemy collects all Base subclasses.

# Builds SQL statements for each (CREATE TABLE users (...), etc.).

# Executes them against the connected PostgreSQL DB.