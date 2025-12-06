# api/controller_schemas/responses/project_responses.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ProjectResponse(BaseModel):
    """Response model for a project"""
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        example = {
            "id": 1,
            "name": "My Project",
            "description": "A sample project description",
            "created_at": "2025-12-06T10:00:00",
            "updated_at": "2025-12-06T10:00:00"
        }
