from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.task import Task, TaskStatus
from app.repositories.base import BaseRepository
from app.exceptions.repository_exceptions import TaskNotFoundError

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db_session: Session):
        super().__init__(Task, db_session)
    
    def get_by_project(self, project_id: int) -> List[Task]:
        return self.db_session.query(Task).filter(
            Task.project_id == project_id
        ).order_by(Task.created_at).all()
    
    def get_overdue_tasks(self) -> List[Task]:
        return self.db_session.query(Task).filter(
            and_(
                Task.deadline < datetime.now(),
                Task.status != TaskStatus.DONE,
                Task.closed_at.is_(None)
            )
        ).all()
    
    def close_overdue_task(self, task_id: int) -> Task:
        task = self.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        
        task.status = TaskStatus.DONE
        task.closed_at = datetime.now()
        return self.update(task)
    
    def count_by_project(self, project_id: int) -> int:
        return self.db_session.query(Task).filter(Task.project_id == project_id).count()