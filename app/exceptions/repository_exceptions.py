from .base import ToDoListException

class RepositoryException(ToDoListException):
    """Base repository exception"""
    pass

class ProjectNotFoundError(RepositoryException):
    """Raised when project is not found"""
    pass

class TaskNotFoundError(RepositoryException):
    """Raised when task is not found"""
    pass

class DuplicateProjectError(RepositoryException):
    """Raised when project name already exists"""
    pass