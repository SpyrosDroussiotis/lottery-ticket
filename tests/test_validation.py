import pytest
from pydantic import ValidationError

from app.models import TicketSubmission


def test_valid_ticket_passes_validation():
    ticket = TicketSubmission(
        draw_id="DRAW-2026-0625",
        player_id="player-42",
        numbers=[3, 12, 17, 25, 33, 41],
        stake=5.0,
    )

    assert ticket.draw_id == "DRAW-2026-0625"
    assert ticket.player_id == "player-42"
    assert ticket.numbers == [3, 12, 17, 25, 33, 41]
    assert ticket.stake == 5.0


def test_empty_draw_id_fails_validation():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="",
            player_id="player-42",
            numbers=[3, 12, 17, 25, 33, 41],
            stake=5.0,
        )


def test_empty_player_id_fails_validation():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="",
            numbers=[3, 12, 17, 25, 33, 41],
            stake=5.0,
        )


def test_numbers_must_contain_exactly_six_values():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="player-42",
            numbers=[1, 2, 3],
            stake=5.0,
        )


def test_numbers_must_be_unique():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="player-42",
            numbers=[1, 2, 3, 4, 5, 5],
            stake=5.0,
        )


def test_numbers_must_be_between_1_and_45():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="player-42",
            numbers=[1, 2, 3, 4, 5, 46],
            stake=5.0,
        )


def test_stake_must_be_at_least_one():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="player-42",
            numbers=[1, 2, 3, 4, 5, 6],
            stake=0.5,
        )


def test_stake_must_not_exceed_500():
    with pytest.raises(ValidationError):
        TicketSubmission(
            draw_id="DRAW-2026-0625",
            player_id="player-42",
            numbers=[1, 2, 3, 4, 5, 6],
            stake=600,
        )