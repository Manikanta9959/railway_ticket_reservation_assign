from db.session import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship




# Models
class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)  # Confirmed, RAC, Waiting
    berth_type = Column(String, nullable=True)  # Lower, Middle, Upper, Side-Lower
    passenger = relationship("Passenger", backref="ticket", uselist=False)
    
    

