from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project import Project
from app.repositories.base import BaseRepository
from app.exceptions.repository_exceptions import ProjectNotFoundError, DuplicateProjectError

class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db_session: Session):
        super().__init__(Project, db_session)
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.db_session.query(Project).filter(Project.name == name).first()
    
    def get_all_ordered(self) -> List[Project]:
        return self.db_session.query(Project).order_by(Project.created_at).all()
    
    def create(self, project: Project) -> Project:
        # Check for duplicate name
        if self.get_by_name(project.name):
            raise DuplicateProjectError(f"Project with name '{project.name}' already exists")
        
        return super().create(project)
    
    def update(self, project: Project) -> Project:
        # Check for duplicate name
        existing = self.db_session.query(Project).filter(
            Project.name == project.name,
            Project.id != project.id
        ).first()
        
        if existing:
            raise DuplicateProjectError(f"Project with name '{project.name}' already exists")
        
        return super().update(project)
    
    def get_with_tasks(self, project_id: int) -> Optional[Project]:
        return self.db_session.query(Project).filter(Project.id == project_id).first()