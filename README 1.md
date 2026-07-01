# Take-Home Technical Test: Lottery Draw Ticket Validator

Thank you for taking the time to complete this take-home exercise. This
challenge is designed to evaluate your skills in Python backend development:
data validation, API design with FastAPI, batch processing, and testing.

This task is intentionally aligned with practical backend work in a lottery
system. The focus is on correctness, clarity, and clean structure: validating
inputs, storing state, exposing endpoints, processing batches, and writing
meaningful tests.

Please complete the task at your own pace. We prioritize clean, readable, and
well-tested code over extra features.

Suggested effort: about 2-3 hours. If you run out of time, it is completely
fine to stop after the core requirements and briefly note what you would do
next.

You are welcome to use AI tools (e.g. ChatGPT, Copilot, Cursor) to help you.

---

## The Problem

You are building a small service that validates and processes lottery ticket
submissions for a single draw. Each ticket must pass strict validation before
being accepted, and the service must support both single-ticket submission
via API and batch processing from a JSON file.

A lottery draw has:
- A `draw_id` (string, e.g. `"DRAW-2026-0625"`)
- Valid number range: **1 to 45**
- Each ticket selects exactly **6 unique numbers**
- Each ticket has a `stake` (positive number, minimum 1.00, maximum 500.00)
- Each ticket has a `player_id` (non-empty string)

---

## What to Build

**1. Validation logic**

Create a validation function or Pydantic model that enforces these rules on a
ticket submission:

```json
{
    "draw_id": "DRAW-2026-0625",
    "player_id": "player-42",
    "numbers": [3, 12, 17, 25, 33, 41],
    "stake": 5.00
}
```

Rules:
- `draw_id` must be a non-empty string
- `player_id` must be a non-empty string
- `numbers` must contain exactly 6 integers, all unique, each between 1 and 45
- `stake` must be a number >= 1.00 and <= 500.00

Return clear, specific error messages for each validation failure.

**2. REST API**

Build a FastAPI service with two endpoints:

- `POST /tickets` — accepts a JSON ticket submission. Returns:
  - `201 Created` with the stored ticket (including a generated `ticket_id`)
    on success
  - `422 Unprocessable Entity` with validation error details on failure

- `GET /tickets?draw_id=DRAW-2026-0625` — returns all stored tickets for the
  given draw, ordered by submission time.

Storage: in-memory (a list or dict) is fine — no database required.

**3. Batch processing**

Create a function that accepts a list of ticket submissions (loaded from the
provided `tickets.json`) and returns a summary:

```python
def process_batch(tickets: list[dict]) -> dict:
    """
    Returns:
    - total_submitted: number of tickets in the batch
    - valid: number that passed validation
    - invalid: number that failed validation
    - total_stake: sum of stakes for valid tickets only
    - errors: list of {"index": int, "errors": list[str]} for invalid tickets
    """
```

**4. Async ticket enrichment**

After a ticket is validated and stored, it needs to be "enriched" by checking
the player's eligibility and the draw's availability. In production these would
be external HTTP calls; here, simulate them with async functions that sleep
briefly:

```python
import asyncio

async def check_player_eligible(player_id: str) -> bool:
    """Simulate a remote eligibility check (50ms latency)."""
    await asyncio.sleep(0.05)
    return True  # always eligible for now

async def check_draw_open(draw_id: str) -> bool:
    """Simulate a remote draw-status check (50ms latency)."""
    await asyncio.sleep(0.05)
    return True  # always open for now
```

Requirements:
- Run both checks **concurrently** using `asyncio.gather` so the total wait
  is ~50ms, not ~100ms.
- Call these checks inside your `POST /tickets` endpoint after validation but
  before storing the ticket.
- If either check returns `False`, return `403 Forbidden` with a clear message.
- Add a test that verifies both checks run concurrently (total time < 80ms).

**5. Tests**

Write tests (using `pytest`) that cover:
- A valid ticket passes validation
- Each validation rule rejects bad input (at least one test per rule)
- The API returns 201 for a valid submission
- The API returns 422 with error details for an invalid submission
- The batch processor correctly counts valid/invalid and sums stakes
- The GET endpoint returns tickets filtered by draw_id
- The async enrichment checks run concurrently (elapsed time < 80ms)

**6. Bonus (optional)**

Pick one or more if you have time:
- **Duplicate detection:** reject a ticket if the same `player_id` already
  submitted the exact same numbers for the same draw. Return `409 Conflict`.
- **Draw result checker:** given winning numbers, add a
  `GET /results?draw_id=...` endpoint that returns each ticket with a
  `matched_numbers` count and prize tier (6=jackpot, 5=second, 4=third,
  3=free ticket, else=no win).
- **Logging:** add structured logging (JSON) for each submission showing
  timestamp, player_id, draw_id, and outcome (accepted/rejected).
- **Containerisation:** add a `Dockerfile` that runs the service.

---

## Core Requirements vs Stretch Goals

**Core requirements**
- Correct validation logic with clear error messages
- Working FastAPI endpoints with proper status codes
- Batch processing function with accurate counts
- Concurrent async enrichment using `asyncio.gather`
- Focused automated tests covering happy and unhappy paths

**Stretch goals**
- Duplicate detection
- Draw result checker
- Structured logging
- Particularly clean code structure (separate modules for validation, API,
  batch processing)

## What We Look For

- Correct validation logic covering all specified rules
- Clean API design with proper HTTP status codes and error responses
- Correct use of `async def`, `await`, and `asyncio.gather` for concurrency
- Well-structured Python code with type hints
- Focused tests that cover both valid and invalid cases
- Clear separation between validation, API, and processing logic
- Readable code that explains itself without excessive comments

## What to Submit

- A zip or Git repository containing your solution.
- At minimum: your Python source file(s), test file(s), and the provided
  `tickets.json`.
- Include a `pyproject.toml` or `requirements.txt` so we can install
  dependencies and run your code with one or two commands.
- Optionally include a brief section at the end of this file or in comments
  explaining any design decisions.

## Next Step

Once you have finished, we will arrange a short, informal conversation where
you can walk us through your solution and share how you approached it. This is
simply an opportunity to discuss your ideas together, not a test.

---

## Features Completed

### Core Requirements

- Correct validation logic with clear error messages
- Working FastAPI endpoints with proper status codes
- Batch processing function with accurate counts
- Concurrent async enrichment using `asyncio.gather`
- Focused automated tests covering happy and unhappy paths

### Bonus Features

- Duplicate detection
- Draw result checker
- Structured logging
- Particularly clean code structure (separate modules for validation, API,
  batch processing)


## Project Structure

app/
│
├── main.py
├── models.py
├── storage.py
├── services.py
├── batch.py
├── results.py
└── logs.py
tests/
tickets.json
Dockerfile
requirements.txt

## Installation

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

## Run the API

uvicorn app.main:app --reload

Swagger UI:
http://127.0.0.1:8000/docs

## Run the Tests

python -m pytest


## Docker

docker build -t lottery-ticket .

docker run -p 8000:8000 lottery-ticket