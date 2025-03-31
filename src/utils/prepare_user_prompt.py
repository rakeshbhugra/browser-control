from src.sqlite_manager.manager import sqlite_manager
from src.interfaces.events import Event
from typing import List

async def prepare_user_prompt(user_input: str, user_id: str) -> str:
    # get history for this user_id
    history: List[Event] = await sqlite_manager.get_previous_events(user_id)

    # prepare the user prompt
    user_prompt = ""
    for event in history:
        user_prompt += f"{event.role}: {event.content}\n"
    return user_prompt
