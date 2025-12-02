from typing import List
from app.exceptions.service_exceptions import ValidationError

class ProjectValidator:
    MAX_NAME_LENGTH = 30
    MAX_DESCRIPTION_LENGTH = 150
    
    @classmethod
    def validate_name(cls, name: str, existing_names: List[str] = None) -> None:
        """Validate project name"""
        if not name or not name.strip():
            raise ValidationError("Project name cannot be empty")
        
        if len(name) > cls.MAX_NAME_LENGTH:
            raise ValidationError(f"Project name cannot exceed {cls.MAX_NAME_LENGTH} characters")
        
        if existing_names and name in existing_names:
            raise ValidationError(f"Project name '{name}' already exists")
    
    @classmethod
    def validate_description(cls, description: str) -> None:
        """Validate project description"""
        if not description or not description.strip():
            raise ValidationError("Project description cannot be empty")
        
        if len(description) > cls.MAX_DESCRIPTION_LENGTH:
            raise ValidationError(f"Project description cannot exceed {cls.MAX_DESCRIPTION_LENGTH} characters")
    
    @classmethod
    def validate_project_limits(cls, current_count: int, max_allowed: int) -> None:
        """Validate project count limits"""
        if current_count >= max_allowed:
            raise ValidationError(f"Cannot exceed maximum of {max_allowed} projects")