"""
Application main module
"""

from app.db.session import db_session

def init_database():
    """Initialize database tables"""
    db_session.create_tables()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")