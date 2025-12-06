# api/controllers/task_controller.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.services.task_service import TaskService
from app.models.task import TaskStatus
from app.exceptions.repository_exceptions import TaskNotFoundError, ProjectNotFoundError
from app.exceptions.service_exceptions import LimitExceededError
from app.exceptions.base import ToDoListException
from api.controller_schemas.requests import CreateTaskRequest, UpdateTaskRequest, UpdateTaskStatusRequest
from api.controller_schemas.responses import TaskResponse
from typing import List


class TaskController:
    """Controller for handling task operations"""
    
    def __init__(self, db_session: Session):
        self.task_service = TaskService(db_session)
    
    def create_task(self, request: CreateTaskRequest) -> TaskResponse:
        """Create a new task"""
        try:
            task = self.task_service.create_task(
                project_id=request.project_id,
                title=request.title,
                description=request.description,
                deadline=request.deadline
            )
            return TaskResponse.from_orm(task)
        except ProjectNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except LimitExceededError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except ToDoListException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def get_project_tasks(self, project_id: int) -> List[TaskResponse]:
        """Get all tasks for a specific project"""
        try:
            tasks = self.task_service.get_project_tasks(project_id)
            return [TaskResponse.from_orm(task) for task in tasks]
        except ProjectNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve tasks"
            )
    
    def get_task(self, task_id: int) -> TaskResponse:
        """Get a specific task by ID"""
        try:
            task = self.task_service.get_task(task_id)
            return TaskResponse.from_orm(task)
        except TaskNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    
    def update_task_status(self, task_id: int, request: UpdateTaskStatusRequest) -> TaskResponse:
        """Update task status"""
        try:
            # Convert string status to TaskStatus enum
            status_map = {
                "todo": TaskStatus.TODO,
                "doing": TaskStatus.DOING,
                "done": TaskStatus.DONE
            }
            
            if request.status.lower() not in status_map:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(status_map.keys())}"
                )
            
            new_status = status_map[request.status.lower()]
            task = self.task_service.update_task_status(task_id, new_status)
            return TaskResponse.from_orm(task)
        except TaskNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ToDoListException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def update_task(self, task_id: int, request: UpdateTaskRequest) -> TaskResponse:
        """Update an existing task"""
        try:
            # Convert string status to TaskStatus enum
            status_map = {
                "todo": TaskStatus.TODO,
                "doing": TaskStatus.DOING,
                "done": TaskStatus.DONE
            }
            
            if request.status.lower() not in status_map:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status. Must be one of: {', '.join(status_map.keys())}"
                )
            
            new_status = status_map[request.status.lower()]
            task = self.task_service.update_task(
                task_id=task_id,
                title=request.title,
                description=request.description,
                deadline=request.deadline,
                status=new_status
            )
            return TaskResponse.from_orm(task)
        except TaskNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except ToDoListException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    def delete_task(self, task_id: int) -> dict:
        """Delete a task"""
        try:
            self.task_service.delete_task(task_id)
            return {"message": f"Task {task_id} deleted successfully"}
        except TaskNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete task"
            )
