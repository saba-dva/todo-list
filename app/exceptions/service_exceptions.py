from .base import ToDoListException

class ValidationError(ToDoListException):
    """Raised when validation fails"""
    pass

class LimitExceededError(ToDoListException):
    """Raised when maximum number of projects/tasks is exceeded"""
    pass