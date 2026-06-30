import json
from pathlib import Path
from app.batch import process_batch

def test_process_batch_with_ticket_json():
    file_path= Path("tickets.json")
    
    with file_path.open("r") as file:
        tickets=json.load(file)
        
        result = process_batch(tickets)
        
        assert result["total_submitted"] == 15
        assert result["valid"] == 8
        assert result["invalid"] == 7
        assert result["total_stake"] == 201.0
        assert len(result["errors"]) == 7