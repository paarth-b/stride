"""
Database connection and session management
"""
import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://stride_user:stride_password@localhost:5432/stride_db")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",  # Only log SQL in debug mode
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10
)


def create_db_and_tables():
    """Create all tables defined in models"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session
