#app/models/__init__.py
from .user import User
from .status import Status
from .source import Source
from .tag import Tag, application_tags
from .application import Application
from .update import Update


# This file imports all models so that when you 
# import app.models, SQLAlchemy knows about every table
#  before you call Base.metadata.create_all().