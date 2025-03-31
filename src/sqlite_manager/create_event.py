from src.interfaces.events import Event
from src.sqlite_manager.setup_sql import SessionLocal

async def create_event(event: Event) -> bool:
    try:
        session = SessionLocal()
        session.add(event)
        session.commit()
        session.close()
        return True
    except Exception as e:
        print(e)
        raise e
