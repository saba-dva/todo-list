from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSession:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        
        # Provide a default SQLite URL if DATABASE_URL is not set
        if not self.database_url:
            self.database_url = "sqlite:///todolist.db"
            print(f"Using default database URL: {self.database_url}")
        
        print(f"Database URL: {self.database_url}")  # Debug line
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def create_tables(self):
        from app.models.base import Base
        Base.metadata.create_all(bind=self.engine)

# Global database session instance
db_session = DatabaseSession()