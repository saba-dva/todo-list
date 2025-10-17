import re
from datetime import datetime
from typing import Optional
from .exceptions import ValidationError

class Validator:
    MAX_PROJECT_NAME_LENGTH = 30
    MAX_PROJECT_DESCRIPTION_LENGTH = 150
    MAX_TASK_TITLE_LENGTH = 30
    MAX_TASK_DESCRIPTION_LENGTH = 150
    
    @classmethod
    def validate_task_title(cls, title: str) -> None:
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")
        
        if len(title) > cls.MAX_TASK_TITLE_LENGTH:
            raise ValidationError(f"Task title cannot exceed {cls.MAX_TASK_TITLE_LENGTH} characters")
    
    @classmethod
    def validate_task_description(cls, description: str) -> None:
        if not description or not description.strip():
            raise ValidationError("Task description cannot be empty")
        
        if len(description) > cls.MAX_TASK_DESCRIPTION_LENGTH:
            raise ValidationError(f"Task description cannot exceed {cls.MAX_TASK_DESCRIPTION_LENGTH} characters")
    
    @classmethod
    def validate_deadline(cls, deadline: Optional[datetime]) -> None:
        if deadline and deadline < datetime.now():
            raise ValidationError("Deadline cannot be in the past")
    
    @classmethod
    def validate_task_status(cls, status: str) -> None:
        valid_statuses = ['todo', 'doing', 'done']
        if status not in valid_statuses:
            raise ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")