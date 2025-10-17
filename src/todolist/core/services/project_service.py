from typing import List
from datetime import datetime
import uuid

from ..core.entities.project import Project
from ..core.exceptions import (
    ProjectNotFoundError, 
    DuplicateProjectError, 
    ValidationError
)
from ..core.validators import Validator
from ..storage.in_memory_storage import InMemoryStorage


class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
    
    def create_project(self, name: str, description: str) -> Project:
        # Validate inputs
        existing_names = [p.name for p in self.storage.get_all_projects()]
        Validator.validate_project_name(name, existing_names)
        Validator.validate_project_description(description)
        
        # Create project
        project_id = str(uuid.uuid4())
        now = datetime.now()
        project = Project(
            id=project_id,
            name=name,
            description=description,
            created_at=now,
            updated_at=now
        )
        
        self.storage.create_project(project)
        return project
    
    def get_project(self, project_id: str) -> Project:
        project = self.storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        return project
    
    def update_project(self, project_id: str, name: str, description: str) -> Project:
        project = self.get_project(project_id)
        
        # Validate new name (exclude current project from duplicate check)
        existing_names = [p.name for p in self.storage.get_all_projects() if p.id != project_id]
        Validator.validate_project_name(name, existing_names)
        Validator.validate_project_description(description)
        
        project.update(name, description)
        self.storage.update_project(project)
        return project