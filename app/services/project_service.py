from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository
from app.validators.project_validators import ProjectValidator
from app.exceptions.service_exceptions import LimitExceededError
from app.exceptions.repository_exceptions import ProjectNotFoundError, DuplicateProjectError
import os

class ProjectService:
    def __init__(self, db_session: Session):
        self.project_repo = ProjectRepository(db_session)
        self.task_repo = TaskRepository(db_session)
        self.max_projects = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 100))
    
    def create_project(self, name: str, description: str) -> Project:
        # Validate inputs using validators
        ProjectValidator.validate_name(name)
        ProjectValidator.validate_description(description)
        
        # Check project limit
        projects = self.project_repo.get_all()
        ProjectValidator.validate_project_limits(len(projects), self.max_projects)
        
        project = Project(
            name=name,
            description=description
        )
        
        return self.project_repo.create(project)
    
    def get_project(self, project_id: int) -> Project:
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project
    
    def get_all_projects(self) -> List[Project]:
        return self.project_repo.get_all_ordered()
    
    def update_project(self, project_id: int, name: str, description: str) -> Project:
        project = self.get_project(project_id)
        
        # Validate new inputs using validators
        ProjectValidator.validate_name(name)
        ProjectValidator.validate_description(description)
        
        project.name = name
        project.description = description
        project.updated_at = datetime.now()
        
        return self.project_repo.update(project)
    
    def delete_project(self, project_id: int) -> None:
        project = self.get_project(project_id)
        self.project_repo.delete(project_id)