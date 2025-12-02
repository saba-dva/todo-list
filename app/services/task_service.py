from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.validators.task_validators import TaskValidator
from app.exceptions.service_exceptions import LimitExceededError
from app.exceptions.repository_exceptions import ProjectNotFoundError, TaskNotFoundError
import os

class TaskService:
    def __init__(self, db_session: Session):
        self.task_repo = TaskRepository(db_session)
        self.project_repo = ProjectRepository(db_session)
        self.max_tasks_per_project = int(os.getenv('MAX_NUMBER_OF_TASKS', 1000))
    
    def create_task(
        self, 
        project_id: int, 
        title: str, 
        description: str, 
        deadline: Optional[datetime] = None
    ) -> Task:
        # Verify project exists
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        
        # Validate inputs using validators
        TaskValidator.validate_title(title)
        TaskValidator.validate_description(description)
        TaskValidator.validate_deadline(deadline)
        
        # Check task limit for project
        task_count = self.task_repo.count_by_project(project_id)
        TaskValidator.validate_task_limits(task_count, self.max_tasks_per_project)
        
        task = Task(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            status=TaskStatus.TODO
        )
        
        return self.task_repo.create(task)
    
    def get_task(self, task_id: int) -> Task:
        task = self.task_repo.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return task
    
    def get_project_tasks(self, project_id: int) -> List[Task]:
        # Verify project exists
        project = self.project_repo.get(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        
        return self.task_repo.get_by_project(project_id)
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> Task:
        task = self.get_task(task_id)
        
        # Validate status using validator
        TaskValidator.validate_status(status)
        
        task.status = status
        task.updated_at = datetime.now()
        
        return self.task_repo.update(task)
    
    def update_task(
        self, 
        task_id: int, 
        title: str, 
        description: str, 
        deadline: Optional[datetime],
        status: TaskStatus
    ) -> Task:
        task = self.get_task(task_id)
        
        # Validate all inputs using validators
        TaskValidator.validate_title(title)
        TaskValidator.validate_description(description)
        TaskValidator.validate_deadline(deadline)
        TaskValidator.validate_status(status)
        
        task.title = title
        task.description = description
        task.deadline = deadline
        task.status = status
        task.updated_at = datetime.now()
        
        return self.task_repo.update(task)
    
    def delete_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.task_repo.delete(task_id)
    
    def get_overdue_tasks(self) -> List[Task]:
        return self.task_repo.get_overdue_tasks()
    
    def close_overdue_task(self, task_id: int) -> Task:
        return self.task_repo.close_overdue_task(task_id)