from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv('DATABASE_URL')

engine = create_engine(db)

@event.listens_for(engine, "connect")
def set_timezone(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET TIME ZONE 'UTC'")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()