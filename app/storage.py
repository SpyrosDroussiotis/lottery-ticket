from datetime import datetime, UTC
from uuid import uuid4

from app.models import TicketSubmission, StoredTicket

tickets: list[StoredTicket] = []


def store_ticket(ticket: TicketSubmission) -> StoredTicket:
    stored_ticket = StoredTicket(
        ticket_id=str(uuid4()),
        draw_id = ticket.draw_id,
        player_id = ticket.player_id,
        numbers = ticket.numbers,
        stake = ticket.stake,
        submitted_at = datetime.now(UTC), 
    )
    
    tickets.append(stored_ticket)
    
    return stored_ticket

def get_tickets_by_draw(draw_id: str) -> list[StoredTicket]:
    return [ticket for ticket in tickets if ticket.draw_id == draw_id]

def ticket_exists(ticket: TicketSubmission) -> bool:
    return any(
        store_ticketd.draw_id == ticket.draw_id
        and store_ticketd.player_id == ticket.player_id
        and store_ticketd.numbers == ticket.numbers
        for store_ticketd in tickets
    )