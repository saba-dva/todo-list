from typing import List, Optional
from datetime import datetime
import uuid

from ..core.entities.task import Task, TaskStatus
from ..core.exceptions import TaskNotFoundError, ValidationError
from ..core.validators import Validator
from ..storage.in_memory_storage import InMemoryStorage
from .project_service import ProjectService

class TaskService:
    def __init__(self, storage: InMemoryStorage, project_service: ProjectService):
        self.storage = storage
        self.project_service = project_service
    
    def create_task(
        self, 
        project_id: str, 
        title: str, 
        description: str, 
        deadline: Optional[datetime] = None
    ) -> Task:
        self.project_service.get_project(project_id)
        
        Validator.validate_task_title(title)
        Validator.validate_task_description(description)
        Validator.validate_deadline(deadline)
        
        task_id = str(uuid.uuid4())
        now = datetime.now()
        task = Task(
            id=task_id,
            project_id=project_id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            deadline=deadline,
            created_at=now,
            updated_at=now
        )
        
        self.storage.create_task(task)
        return task
    
    def update_task_status(self, task_id: str, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        
        if not isinstance(status, TaskStatus):
            raise ValidationError("Invalid task status")
        
        task.update_status(status)
        self.storage.update_task(task)
        return task
    
    def get_task(self, task_id: str) -> Task:
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task
    
    def update_task(
        self, 
        task_id: str, 
        title: str, 
        description: str, 
        deadline: Optional[datetime],
        status: TaskStatus
    ) -> Task:
        task = self.get_task(task_id)
        
        Validator.validate_task_title(title)
        Validator.validate_task_description(description)
        Validator.validate_deadline(deadline)
        
        task.update_details(title, description, deadline)
        task.status = status
        self.storage.update_task(task)
        return task
    
    def delete_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        self.storage.delete_task(task_id)