import asyncio

async def check_player_eligible(player_id: str) -> bool:
    await asyncio.sleep(0.05)
    return True

async def check_draw_open(draw_id: str) -> bool:
    await asyncio.sleep(0.05)
    return True

async def validate_ticket(player_id: str, draw_id: str) -> bool:
    draw_open, player_eligible = await asyncio.gather(
        check_draw_open(draw_id),
        check_player_eligible(player_id),
    )
    
    return player_eligible and draw_open