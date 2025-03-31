from src.interfaces.events import Event
from src.sqlite_manager.setup_sql import SessionLocal
from src.sqlite_manager.create_events_db import EventsDB
import json

async def create_event(event: Event) -> bool:
    try:
        session = SessionLocal()
        
        # Convert Event to EventsDB
        event_db = EventsDB(
            user_id=event.user_id,
            role=event.role,
            content=event.content,
            message_type=event.message_type,
            function_name=event.function_details.name if event.function_details else None,
            function_args=json.dumps(event.function_details.args) if event.function_details else None,
            function_response=event.function_details.response if event.function_details else None,
            event_timestamp=event.event_timestamp
        )
        
        session.add(event_db)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
        raise e
