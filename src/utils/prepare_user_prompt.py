from src.sqlite_manager.manager import sqlite_manager
from src.interfaces.events import Event
from typing import List
from src.interfaces.context import Context
import os
async def prepare_user_prompt(context: Context) -> str:
    # get history for this user_id
    history: List[Event] = await sqlite_manager.get_previous_events(context.user_id)

    # prepare the user prompt
    user_prompt = "<conversation>\n"
    for event in history:
        user_prompt += f"{event.role}: {event.content}\n"
    user_prompt += "</conversation>\n"
    
    with open(os.path.join("data/gitignored", "user_prompt.txt"), 'w') as f:
        f.write(user_prompt)
    
    return user_prompt
