from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    last_name = Column(String(50))
    first_name = Column(String(50))
    middle_name = Column(String(50))
    email = Column(String(100), unique=True)
    telegram_id = Column(String(50), unique=True)
    role = Column(String(20))

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()