from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine("sqlite:///events.db")  # Creates events.db file
SessionLocal = sessionmaker(bind=engine)
