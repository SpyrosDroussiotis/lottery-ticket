from fastapi import FastAPI, HTTPException, status

from app.models import StoredTicket, TicketSubmission, TicketResult
from app.services import validate_ticket
from app.storage import store_ticket, get_tickets_by_draw, ticket_exists
from app.logs import log_submission
from app.results import calculate_results

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
        log_submission(ticket.player_id, ticket.draw_id, "rejected")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Player is not eligible or draw not open"
        )
        
    if ticket_exists(ticket):
        log_submission(ticket.player_id, ticket.draw_id, "rejected")
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail= "Duplicate ticket submission"
        )
        
    stored_ticket = store_ticket(ticket)
    log_submission(ticket.player_id, ticket.draw_id, "accepted")
    return stored_ticket

@app.get("/tickets", response_model=list[StoredTicket])
def list_tickets(draw_id: str):
    return get_tickets_by_draw(draw_id)

@app.get("/results", response_model=list[TicketResult])
def get_results(draw_id: str):
    winning_numbers = [4,12,17,25,33,41]
    tickets= get_tickets_by_draw(draw_id)
    
    return calculate_results(tickets, winning_numbers
    )
