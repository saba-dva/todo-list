# api/controller_schemas/requests/project_requests.py
from pydantic import BaseModel, Field
from typing import Optional


class CreateProjectRequest(BaseModel):
    """Request model for creating a new project"""
    name: str = Field(..., min_length=1, max_length=30, description="Project name")
    description: str = Field(..., min_length=1, description="Project description")

    class Config:
        example = {
            "name": "My Project",
            "description": "A sample project description"
        }


class UpdateProjectRequest(BaseModel):
    """Request model for updating an existing project"""
    name: str = Field(..., min_length=1, max_length=30, description="Project name")
    description: str = Field(..., min_length=1, description="Project description")

    class Config:
        example = {
            "name": "Updated Project",
            "description": "Updated description"
        }
