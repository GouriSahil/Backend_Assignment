from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a database engine
# - Using SQLite as the database with the file `fitness_booking.db`.
# - The `check_same_thread` argument is set to False to allow multiple threads to interact with the database.
engine = create_engine("sqlite:///fitness_booking.db", connect_args={"check_same_thread": False})

# Create a session factory
# - `autocommit=False`: Ensures that changes are not automatically committed to the database.
# - `autoflush=False`: Prevents automatic flushing of changes to the database.
# - `bind=engine`: Binds the session to the database engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
# - All database models will inherit from this base class.
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.
    - Creates a new session for each request.
    - Ensures the session is properly closed after the request is completed.
    - Used as a dependency in FastAPI endpoints to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()