from datetime import datetime

from pydantic import BaseModel, Field, field_validator 



class TicketSubmission(BaseModel):
    draw_id: str
    player_id: str
    numbers: list[int]
    stake: float = Field(..., ge=1.0, le=500.0)
    
    @field_validator("draw_id")
    @classmethod
    def validate_draw_id(cls , value: str) -> str:
        if not value.strip():
            raise ValueError("draw_id cannot be empty")
        
        return value
        
    @field_validator("player_id")
    @classmethod
    def validate_player_id(cls , value: str) -> str:
        if not value.strip():
            raise ValueError("player_id cannot be empty")
        
        return value
        
    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls , value: list[int]) -> list[int]:
        if len(value) != 6:
            raise ValueError("Exactly 6 numbers are required")
        
        if len(set(value)) != 6:
            raise ValueError("Numbers must be unique")
        
        for number in value:
            if number < 1 or number > 45:
                raise ValueError("Numbers must be between 1 and 45")
            
        return value
    
class StoredTicket(TicketSubmission):
    ticket_id: str
    submitted_at: datetime
    
class TicketResult(StoredTicket):
    matched_numbers: int
    prize_tier: str

    