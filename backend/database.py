from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./pictalk.db"

# Connection to database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Creates queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()