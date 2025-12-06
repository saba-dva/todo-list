# api/controller_schemas/requests/task_requests.py
from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from datetime import datetime, date


class CreateTaskRequest(BaseModel):
    """Request model for creating a new task"""
    project_id: int = Field(..., gt=0, description="Project ID")
    title: str = Field(..., min_length=1, max_length=30, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    deadline: Optional[Union[datetime, date]] = Field(None, description="Task deadline (optional). Format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS")

    @validator('deadline', pre=True, always=False)
    def parse_deadline(cls, v):
        """Convert date to datetime if needed"""
        if isinstance(v, str):
            # Try parsing as date first (YYYY-MM-DD)
            try:
                parsed_date = datetime.strptime(v, "%Y-%m-%d").date()
                return datetime.combine(parsed_date, datetime.min.time())
            except ValueError:
                pass
            # Fall back to datetime parsing
            return v
        elif isinstance(v, date) and not isinstance(v, datetime):
            # Convert date object to datetime
            return datetime.combine(v, datetime.min.time())
        return v

    class Config:
        example = {
            "project_id": 1,
            "title": "Complete project setup",
            "description": "Set up the project infrastructure",
            "deadline": "2025-12-31"
        }


class UpdateTaskStatusRequest(BaseModel):
    """Request model for updating task status"""
    status: str = Field(..., description="Task status: 'todo', 'doing', or 'done'")

    class Config:
        example = {
            "status": "doing"
        }


class UpdateTaskRequest(BaseModel):
    """Request model for updating an existing task"""
    title: str = Field(..., min_length=1, max_length=30, description="Task title")
    description: str = Field(..., min_length=1, description="Task description")
    status: str = Field(..., description="Task status: 'todo', 'doing', or 'done'")
    deadline: Optional[datetime] = Field(None, description="Task deadline (optional)")

    class Config:
        example = {
            "title": "Updated task",
            "description": "Updated description",
            "status": "doing",
            "deadline": "2025-12-31T23:59:59"
        }
