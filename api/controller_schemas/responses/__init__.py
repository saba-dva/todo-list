# api/controller_schemas/responses/__init__.py
from .project_responses import ProjectResponse
from .task_responses import TaskResponse

__all__ = [
    "ProjectResponse",
    "TaskResponse",
    "AutoCloseResponse",
]
