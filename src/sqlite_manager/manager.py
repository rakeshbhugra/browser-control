from src.sqlite_manager.create_events_db import create_events_db
from src.interfaces.events import Event
from src.sqlite_manager.get_previous_events import get_previous_events
from src.sqlite_manager.create_event import create_event
from typing import List

create_events_db()

class SqliteManager:
    def __init__(self):
        pass

    async def create_event(self, event: Event) -> bool:
        return await create_event(event)

    async def get_previous_events(self, user_id: str) -> List[Event]:
        return await get_previous_events(user_id)

sqlite_manager = SqliteManager()