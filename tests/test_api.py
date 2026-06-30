from fastapi.testclient import TestClient

from app.main import app
from app.storage import tickets

client= TestClient(app)

def test_home():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {
        "message":"Lottery Ticket Validator"
    }
   
    
def test_create_ticket_returns_201():
    tickets.clear()
    
    response = client.post(
        "/tickets", json={
            "draw_id": "DRAW-2026-0625",
            "player_id": "player-42",
            "numbers": [3, 12, 17, 25, 33, 41],
            "stake": 5.0,
        },
    )
    
    assert response.status_code == 201
    
    data = response.json()
    assert "ticket_id" in data
    assert "submitted_at" in data
    assert data["draw_id"] == "DRAW-2026-0625"
    assert data["player_id"]=="player-42"
    
def test_create_invalid_ticket_returns_422():
    
    response = client.post(
        "/tickets", json ={
              "draw_id": "DRAW-2026-0625",
            "player_id": "player-42",
            "numbers": [1, 2, 4],
            "stake": 5.0,
        },
    )
    
    assert response.status_code == 422
    
def test_get_tickets_filtered_by_draw_id():
    tickets.clear()
    
    client.post(
        "/tickets", json = {
            "draw_id": "DRAW-1",
            "player_id": "player-1",
            "numbers": [1, 2, 3, 4, 5, 6],
            "stake": 10.0,
        },
    )
    
    client.post(
        "/tickets", json = {
           "draw_id": "DRAW-2",
            "player_id": "player-2",
            "numbers": [7, 8, 9, 10, 11, 12],
            "stake": 20.0,
        },
    )
    
    response = client.get("/tickets?draw_id=DRAW-1")
    
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 1
    assert data[0]["draw_id"]=="DRAW-1"
    
    
def test_duplicate_tickets_returns_409():
    tickets.clear()
    
    payload={
        "draw_id": "DRAW-2026-0625",
        "player_id": "player-42",
        "numbers": [3, 12, 17, 25, 33, 41],
        "stake": 5.0,
    }
    
    first_response = client.post("/tickets", json=payload)
    second_response = client.post("/tickets", json=payload)
    
    assert first_response.status_code == 201
    assert second_response.status_code == 409
    
    assert second_response.json()["detail"] == "Duplicate ticket submission"
    
    
    