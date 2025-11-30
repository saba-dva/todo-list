from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSession:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def create_tables(self):
        from app.models.base import Base
        Base.metadata.create_all(bind=self.engine)

db_session = DatabaseSession()