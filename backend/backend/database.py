from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import settings

SQLALCHEMY_DATABASE_URL = settings.database_url


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=110, max_overflow=20, pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()
metadata = Base.metadata


def init_db():
    # Base.metadata.create_all(bind=engine)
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
