import json
from datetime import UTC, datetime

def log_submission(player_id: str, draw_id: str, outcome: str) -> None:
    log_entry={
        "timestamp": datetime.now(UTC).isoformat(),
        "player_id": player_id,
        "draw_id": draw_id,
        "outcome": outcome,
    }
    
    print(json.dumps(log_entry))