'''import os
import django
from django.conf import settings
from django.db import connections

# Initialize Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")

# Ensure Django is set up only once
if not settings.configured:
    django.setup()

def getdbconnection():
    """
    Return the default Django database connection.
    This ensures that FastAPI can access the same database as Django.
    """
    return connections['default']'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from django.conf import settings
import urllib.parse

# Determine the database URL to use with SQLAlchemy
def get_database_url():
    db_config = settings.DATABASES['default']
    engine = db_config['ENGINE']    
    # For SQLite
    if engine == 'django.db.backends.sqlite3':
        # SQLite requires a file path or :memory: for an in-memory DB
        return f"sqlite:///{db_config['NAME']}"    

    raise ValueError(f"Unsupported database engine: {engine}")

# Create the database engine using the constructed URL
DATABASE_URL = get_database_url()

# Create SQLAlchemy engine and session maker
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

