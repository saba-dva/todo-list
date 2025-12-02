from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus
from app.exceptions.service_exceptions import ValidationError

class TaskValidator:
    MAX_TITLE_LENGTH = 30
    MAX_DESCRIPTION_LENGTH = 150
    
    @classmethod
    def validate_title(cls, title: str) -> None:
        """Validate task title"""
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")
        
        if len(title) > cls.MAX_TITLE_LENGTH:
            raise ValidationError(f"Task title cannot exceed {cls.MAX_TITLE_LENGTH} characters")
    
    @classmethod
    def validate_description(cls, description: str) -> None:
        """Validate task description"""
        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty")
        
        if len(description) > cls.MAX_DESCRIPTION_LENGTH:
            raise ValidationError(f"Task description cannot exceed {cls.MAX_DESCRIPTION_LENGTH} characters")
    
    @classmethod
    def validate_deadline(cls, deadline: Optional[datetime]) -> None:
        """Validate task deadline"""
        if deadline and deadline < datetime.now():
            raise ValidationError("Deadline cannot be in the past")
    
    @classmethod
    def validate_status(cls, status: TaskStatus) -> None:
        """Validate task status"""
        if not isinstance(status, TaskStatus):
            raise ValidationError("Invalid task status provided")
        
        valid_statuses = [TaskStatus.TODO, TaskStatus.DOING, TaskStatus.DONE]
        if status not in valid_statuses:
            raise ValidationError("Status must be one of: todo, doing, done")
    
    @classmethod
    def validate_status_string(cls, status_str: str) -> TaskStatus:
        """Validate string status and return TaskStatus enum"""
        valid_statuses = {
            'todo': TaskStatus.TODO,
            'doing': TaskStatus.DOING, 
            'done': TaskStatus.DONE
        }
        
        if status_str not in valid_statuses:
            raise ValidationError(f"Status must be one of: {', '.join(valid_statuses.keys())}")
        
        return valid_statuses[status_str]
    
    @classmethod
    def validate_task_limits(cls, current_count: int, max_allowed: int) -> None:
        """Validate task count limits"""
        if current_count >= max_allowed:
            raise ValidationError(f"Cannot exceed maximum of {max_allowed} tasks per project")