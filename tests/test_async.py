import time
import pytest

from app.services import validate_ticket

@pytest.mark.asyncio
async def test_async_enrichement_check_runs_concurrently():
    start_time=time.perf_counter()
    
    result = await validate_ticket(player_id = "player-1", draw_id = "DRAW-2026-0625" )
    
    elapsed_time = time.perf_counter() - start_time
    
    assert result is True
    assert elapsed_time < 0.08