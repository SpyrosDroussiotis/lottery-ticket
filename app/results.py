from app.models import StoredTicket, TicketResult


def calculate_results(tickets: list[StoredTicket], winning_numbers: list[int]) -> list[TicketResult]:
    results = []
    
    for ticket in tickets:
        matched_numbers = len(set(ticket.numbers) & set(winning_numbers))
        
        if matched_numbers == 6:
            prize = "Jackpot"
        elif matched_numbers == 5:
            prize = "Second"
        elif matched_numbers == 4:
            prize = "Third"
        elif matched_numbers == 3:
            prize = "Free Ticket"
        else:
            prize = "No win"

        results.append(
            TicketResult(
                **ticket.model_dump(),
                matched_numbers=matched_numbers,
                prize_tier=prize,
            )
        )
        
    return results