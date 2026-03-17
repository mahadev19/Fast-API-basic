from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings                          # ← ADDED

# -------------------------------
# DATABASE SETUP
# — URL loaded from .env instead of hardcoded
# -------------------------------
engine = create_engine(settings.database_url)        # ← CHANGED

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()