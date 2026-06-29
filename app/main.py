from fastapi import FastAPI, HTTPException, status
from app.models import StoredTicket, TicketSubmission
from app.services import validate_ticket
from app.storage import store_ticket, get_tickets_by_draw

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Lottery Ticket Validator"}

@app.post("/tickets",response_model=StoredTicket, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketSubmission):
    is_valid=await validate_ticket(
        player_id=ticket.player_id,
        draw_id=ticket.draw_id,
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Player is not eligible or draw not open"
        )
        
    return store_ticket(ticket)

@app.get("/tickets", response_model=list[StoredTicket])
def list_tickets(draw_id: str):
    return get_tickets_by_draw(draw_id)