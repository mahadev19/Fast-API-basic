from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings

# -------------------------------
# DATABASE SETUP
# -------------------------------
engine = create_engine(settings.DATABASE_URL)     # ← removed SQLite-only connect_args

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()