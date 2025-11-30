from typing import List
from datetime import datetime
import uuid

from ..core.entities.project import Project
from ..exceptions.exceptions import (
    ProjectNotFoundError, 
    DuplicateProjectError, 
    ValidationError
)
from ..validators.validators import Validator
from ..db.in_memory_storage import InMemoryStorage


class ProjectService:
    def __init__(self, storage: InMemoryStorage):
        self.storage = storage
    
    def create_project(self, name: str, description: str) -> Project:
        existing_names = [p.name for p in self.storage.get_all_projects()]
        Validator.validate_project_name(name, existing_names)
        Validator.validate_project_description(description)
        
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
    
    def get_all_projects(self) -> List[Project]:
        return self.storage.get_all_projects()
    
    def update_project(self, project_id: str, name: str, description: str) -> Project:
        project = self.get_project(project_id)
        
        existing_names = [p.name for p in self.storage.get_all_projects() if p.id != project_id]
        Validator.validate_project_name(name, existing_names)
        Validator.validate_project_description(description)
        
        project.update(name, description)
        self.storage.update_project(project)
        return project
    
    def delete_project(self, project_id: str) -> None:
        project = self.get_project(project_id)
        self.storage.delete_project(project_id)