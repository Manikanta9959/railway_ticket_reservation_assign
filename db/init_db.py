from db.session import engine, Base
from models.passenger import Passenger, Ticket  # Ensure models are imported

def init_db():
    print("Creating tables if they don't exist...")
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
