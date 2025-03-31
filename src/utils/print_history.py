from src.sqlite_manager.manager import sqlite_manager
from src.utils.print_helper import print_helper

async def print_history(user_id: str):
    history = await sqlite_manager.get_previous_events(user_id)
    print_helper.line_print(color='green')
    for event in history:
        print(event)
    print_helper.line_print(color='green')