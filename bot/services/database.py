from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models import Base

engine = create_engine('sqlite:///../data/database.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)