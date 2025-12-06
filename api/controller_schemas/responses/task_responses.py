# api/controller_schemas/responses/task_responses.py
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class TaskResponse(BaseModel):
    """Response model for a task"""
    id: int
    project_id: int
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]

    @validator('status', pre=True)
    def convert_status_enum(cls, v):
        """Convert enum to string value"""
        if hasattr(v, 'value'):  # If it's an enum
            return v.value
        return v

    class Config:
        orm_mode = True
        example = {
            "id": 1,
            "project_id": 1,
            "title": "Complete project setup",
            "description": "Set up the project infrastructure",
            "status": "todo",
            "deadline": "2025-12-31T23:59:59",
            "created_at": "2025-12-06T10:00:00",
            "updated_at": "2025-12-06T10:00:00",
            "closed_at": None
        }

