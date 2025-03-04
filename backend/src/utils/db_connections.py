from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
import os

# Create a base class for declarative models
Base = declarative_base()


def create_db_connection(db_url=None):
    """
    Create a database connection and return engine and session

    Args:
        db_url (str, optional): Database connection URL.
                                Defaults to environment variable or PostgreSQL default.

    Returns:
        tuple: SQLAlchemy engine and scoped session
    """
    # Use provided DB URL or fetch from environment
    if not db_url:
        db_url = os.getenv(
            "DATABASE_URL", "postgresql://user:password@localhost/expense_tracker_db"
        )

    try:
        # Create engine with connection pooling and logging
        engine = create_engine(
            db_url,
            pool_size=10,  # Number of connections to keep open
            max_overflow=20,  # Maximum number of connections beyond pool_size
            pool_timeout=30,  # Timeout for getting a connection from the pool
            pool_recycle=1800,  # Recycle connections after 30 minutes
            echo=False,  # Set to True for SQL query logging
        )

        # Create a configured "Session" class
        session_factory = sessionmaker(bind=engine)

        # Create a scoped session to ensure thread-local sessions
        Session = scoped_session(session_factory)

        return engine, Session

    except Exception as e:
        raise ConnectionError(f"Database connection error: {str(e)}")


def init_db(engine):
    """
    Initialize the database by creating all tables

    Args:
        engine: SQLAlchemy engine
    """
    try:
        # Import models to ensure they are registered
        from ..models.user import User
        from ..models.expense import Expense
        from ..models.event import Event

        # Create all tables defined in models
        Base.metadata.create_all(engine)
    except Exception as e:
        raise RuntimeError(f"Database initialization error: {str(e)}")


def drop_db(engine):
    """
    Drop all tables in the database

    Args:
        engine: SQLAlchemy engine
    """
    try:
        # Drop all tables
        Base.metadata.drop_all(engine)
    except Exception as e:
        raise RuntimeError(f"Database drop error: {str(e)}")
