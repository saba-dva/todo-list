class ToDoListException(Exception):
    """Base exception for ToDoList application"""
    pass

class ProjectNotFoundError(ToDoListException):
    """Raised when project is not found"""
    pass

class DuplicateProjectError(ToDoListException):
    """Raised when project name already exists"""
    pass

class ValidationError(ToDoListException):
    """Raised when validation fails"""
    pass

class LimitExceededError(ToDoListException):
    """Raised when maximum number of projects/tasks is exceeded"""
    pass

class TaskNotFoundError(ToDoListException):
    """Raised when task is not found"""
    pass