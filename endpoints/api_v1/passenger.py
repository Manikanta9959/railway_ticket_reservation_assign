
from fastapi import APIRouter, Depends, HTTPException
from models.passenger import Ticket, Passenger
from sqlalchemy.orm import Session

from db.session import get_db

router = APIRouter()

# Constants
TOTAL_CONFIRMED = 63
TOTAL_RAC = 9  # Each RAC berth holds 2 passengers (18 total)
TOTAL_WAITING = 10


def get_ticket_status(db: Session):
    confirmed_count = db.query(Ticket).filter(Ticket.status == "Confirmed").count()
    rac_count = db.query(Ticket).filter(Ticket.status == "RAC").count()
    waiting_count = db.query(Ticket).filter(Ticket.status == "Waiting").count()
    return confirmed_count, rac_count, waiting_count

@router.post("/api/v1/tickets/book")
def book_ticket(name: str, age: int, gender: str, db: Session = Depends(get_db)):
    confirmed_count, rac_count, waiting_count = get_ticket_status(db)
    
    if confirmed_count < TOTAL_CONFIRMED:
        berth_type = "Lower" if (age >= 60 or gender == "Female") else "Upper"
        ticket = Ticket(status="Confirmed", berth_type=berth_type)
    elif rac_count < TOTAL_RAC * 2:
        ticket = Ticket(status="RAC", berth_type="Side-Lower")
    elif waiting_count < TOTAL_WAITING:
        ticket = Ticket(status="Waiting", berth_type=None)
    else:
        raise HTTPException(status_code=400, detail="No tickets available")
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    passenger = Passenger(name=name, age=age, gender=gender, ticket_id=ticket.id)
    db.add(passenger)
    db.commit()
    db.refresh(passenger)

    return {"message": "Ticket booked successfully", "ticket_id": ticket.id, "status": ticket.status}

@router.post("/api/v1/tickets/cancel/{ticket_id}")
def cancel_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    
    # Move RAC to Confirmed, Waiting to RAC
    rac_ticket = db.query(Ticket).filter(Ticket.status == "RAC").first()
    if rac_ticket:
        rac_ticket.status = "Confirmed"
        db.commit()
    
        waiting_ticket = db.query(Ticket).filter(Ticket.status == "Waiting").first()
        if waiting_ticket:
            waiting_ticket.status = "RAC"
            db.commit()
    
    return {"message": "Ticket cancelled successfully"}

@router.get("/api/v1/tickets/booked")
def get_booked_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.status == "Confirmed").all()
    return {"booked_tickets": tickets}

@router.get("/api/v1/tickets/available")
def get_available_tickets(db: Session = Depends(get_db)):
    confirmed_count, rac_count, waiting_count = get_ticket_status(db)
    available_confirmed = TOTAL_CONFIRMED - confirmed_count
    available_rac = (TOTAL_RAC * 2) - rac_count
    available_waiting = TOTAL_WAITING - waiting_count
    return {"available_confirmed": available_confirmed, "available_rac": available_rac, "available_waiting": available_waiting}
