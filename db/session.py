from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Setup
DATABASE_URL = "sqlite:///./railway_reservation.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
# Initialize database
def init_db():
    logger.info("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)

init_db()  # Ensure DB creation occurs before app starts
