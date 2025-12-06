# api/controllers/project_controller.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.exceptions.repository_exceptions import ProjectNotFoundError, DuplicateProjectError
from app.exceptions.service_exceptions import LimitExceededError
from app.exceptions.base import ToDoListException
from api.controller_schemas.requests import CreateProjectRequest, UpdateProjectRequest
from api.controller_schemas.responses import ProjectResponse
from typing import List


class ProjectController:
    """Controller for handling project operations"""
    
    def __init__(self, db_session: Session):
        self.project_service = ProjectService(db_session)
    
    def create_project(self, request: CreateProjectRequest) -> ProjectResponse:
        """Create a new project"""
        try:
            project = self.project_service.create_project(
                name=request.name,
                description=request.description
            )
            return ProjectResponse.from_orm(project)
        except DuplicateProjectError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except LimitExceededError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except ToDoListException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_all_projects(self) -> List[ProjectResponse]:
        """Get all projects"""
        try:
            projects = self.project_service.get_all_projects()
            return [ProjectResponse.from_orm(project) for project in projects]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve projects"
            )
    
    def get_project(self, project_id: int) -> ProjectResponse:
        """Get a specific project by ID"""
        try:
            project = self.project_service.get_project(project_id)
            return ProjectResponse.from_orm(project)
        except ProjectNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    
    def update_project(self, project_id: int, request: UpdateProjectRequest) -> ProjectResponse:
        """Update an existing project"""
        try:
            project = self.project_service.update_project(
                project_id=project_id,
                name=request.name,
                description=request.description
            )
            return ProjectResponse.from_orm(project)
        except ProjectNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except DuplicateProjectError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        except ToDoListException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def delete_project(self, project_id: int) -> dict:
        """Delete a project"""
        try:
            self.project_service.delete_project(project_id)
            return {"message": f"Project {project_id} deleted successfully"}
        except ProjectNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete project"
            )
