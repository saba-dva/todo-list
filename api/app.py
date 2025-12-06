# api/app.py
from fastapi import FastAPI
from api.routers import api_router
from app.db.session import db_session
from app.models.base import Base

app = FastAPI(title="ToDoList API")
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    # dev convenience: create tables (production should use alembic)
    Base.metadata.create_all(bind=db_session.engine)
