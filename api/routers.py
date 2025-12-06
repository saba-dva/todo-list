# api/routers.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.dependencies import get_db
from api.controllers.project_controller import ProjectController
from api.controllers.task_controller import TaskController
from api.controller_schemas.requests import (
    CreateProjectRequest,
    UpdateProjectRequest,
    CreateTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
)
from api.controller_schemas.responses import ProjectResponse, TaskResponse
from typing import List

api_router = APIRouter()


# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@api_router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    tags=["Projects"]
)
def create_project(
    request: CreateProjectRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    
    - **name**: Project name (max 30 characters)
    - **description**: Project description
    """
    controller = ProjectController(db)
    return controller.create_project(request)


@api_router.get(
    "/projects",
    response_model=List[ProjectResponse],
    summary="List all projects",
    tags=["Projects"]
)
def list_projects(db: Session = Depends(get_db)):
    """Get all projects in the system."""
    controller = ProjectController(db)
    return controller.get_all_projects()


@api_router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get a specific project",
    tags=["Projects"]
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get details of a specific project by ID."""
    controller = ProjectController(db)
    return controller.get_project(project_id)


@api_router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    tags=["Projects"]
)
def update_project(
    project_id: int,
    request: UpdateProjectRequest,
    db: Session = Depends(get_db)
):
    """Update an existing project."""
    controller = ProjectController(db)
    return controller.update_project(project_id, request)


@api_router.delete(
    "/projects/{project_id}",
    summary="Delete a project",
    tags=["Projects"]
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project and all its associated tasks."""
    controller = ProjectController(db)
    return controller.delete_project(project_id)


# ============================================================================
# TASK ENDPOINTS
# ============================================================================

@api_router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    tags=["Tasks"]
)
def create_task(
    request: CreateTaskRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new task in a project.
    
    - **project_id**: ID of the project
    - **title**: Task title (max 30 characters)
    - **description**: Task description
    - **deadline**: Optional deadline (ISO 8601 format)
    """
    controller = TaskController(db)
    return controller.create_task(request)


@api_router.get(
    "/projects/{project_id}/tasks",
    response_model=List[TaskResponse],
    summary="Get tasks for a project",
    tags=["Tasks"]
)
def get_project_tasks(project_id: int, db: Session = Depends(get_db)):
    """Get all tasks for a specific project."""
    controller = TaskController(db)
    return controller.get_project_tasks(project_id)


@api_router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    tags=["Tasks"]
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get details of a specific task by ID."""
    controller = TaskController(db)
    return controller.get_task(task_id)


@api_router.patch(
    "/tasks/{task_id}/status",
    response_model=TaskResponse,
    summary="Change task status",
    tags=["Tasks"]
)
def update_task_status(
    task_id: int,
    request: UpdateTaskStatusRequest,
    db: Session = Depends(get_db)
):
    """
    Update the status of a task.
    
    - **status**: One of 'todo', 'doing', or 'done'
    """
    controller = TaskController(db)
    return controller.update_task_status(task_id, request)


@api_router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    tags=["Tasks"]
)
def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    - **title**: Task title
    - **description**: Task description
    - **status**: One of 'todo', 'doing', or 'done'
    - **deadline**: Optional deadline (ISO 8601 format)
    """
    controller = TaskController(db)
    return controller.update_task(task_id, request)


@api_router.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    tags=["Tasks"]
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a specific task."""
    controller = TaskController(db)
    return controller.delete_task(task_id)