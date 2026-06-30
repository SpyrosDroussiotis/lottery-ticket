from pydantic import ValidationError

from app.models import TicketSubmission

def process_batch(tickets: list[dict])->dict:
    total_submitted = len(tickets)
    valid = 0
    invalid = 0
    total_stake = 0
    errors = []
    
    for index, ticket_data in enumerate(tickets):
        try:
            ticket = TicketSubmission(**ticket_data)
            valid += 1
            total_stake += ticket.stake
            
        except ValidationError as error:
            invalid+=1
            errors.append({
                "index":index,
                "errors": [err["msg"] for err in error.errors()],
            })
            
    return {
        "total_submitted":total_submitted,
        "valid":valid,
        "invalid":invalid,
        "total_stake": total_stake,
        "errors":errors
    }