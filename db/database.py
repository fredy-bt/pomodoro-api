from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()
db = os.getenv('DATABASE_URL')

engine = create_engine(db)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

if __name__ == "__main__":
    with engine.connect() as connection:
        print("Connected successfuly")