from typing import Dict, List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

from ..core.entities.project import Project
from ..core.entities.task import Task, TaskStatus
from ..exceptions.exceptions import LimitExceededError

load_dotenv()

class InMemoryStorage:
    def __init__(self):
        self._projects: Dict[str, Project] = {}
        self._tasks: Dict[str, Task] = {}
        self._project_tasks: Dict[str, List[str]] = {}
        
        self.max_projects = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 100))
        self.max_tasks_per_project = int(os.getenv('MAX_NUMBER_OF_TASKS', 1000))
    
    def create_project(self, project: Project) -> None:
        if len(self._projects) >= self.max_projects:
            raise LimitExceededError(f"Cannot exceed maximum of {self.max_projects} projects")
        
        self._projects[project.id] = project
        self._project_tasks[project.id] = []
    
    def get_project(self, project_id: str) -> Optional[Project]:
        return self._projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        return sorted(
            list(self._projects.values()), 
            key=lambda p: p.created_at
        )
    
    def update_project(self, project: Project) -> None:
        if project.id in self._projects:
            self._projects[project.id] = project
    
    def delete_project(self, project_id: str) -> None:
        if project_id in self._projects:
            task_ids = self._project_tasks.get(project_id, [])
            for task_id in task_ids:
                del self._tasks[task_id]
            
            del self._projects[project_id]
            del self._project_tasks[project_id]
    
    def project_name_exists(self, name: str, exclude_project_id: str = None) -> bool:
        for project in self._projects.values():
            if project.name == name and project.id != exclude_project_id:
                return True
        return False
    
    def create_task(self, task: Task) -> None:
        project_tasks = self._project_tasks.get(task.project_id, [])
        if len(project_tasks) >= self.max_tasks_per_project:
            raise LimitExceededError(f"Cannot exceed maximum of {self.max_tasks_per_project} tasks per project")
        
        self._tasks[task.id] = task
        self._project_tasks[task.project_id].append(task.id)
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self._tasks.get(task_id)
    
    def get_project_tasks(self, project_id: str) -> List[Task]:
        task_ids = self._project_tasks.get(project_id, [])
        tasks = [self._tasks[task_id] for task_id in task_ids if task_id in self._tasks]
        return sorted(tasks, key=lambda t: t.created_at)
    
    def update_task(self, task: Task) -> None:
        if task.id in self._tasks:
            self._tasks[task.id] = task
    
    def delete_task(self, task_id: str) -> None:
        if task_id in self._tasks:
            task = self._tasks[task_id]
            if task.project_id in self._project_tasks:
                self._project_tasks[task.project_id] = [
                    tid for tid in self._project_tasks[task.project_id] 
                    if tid != task_id
                ]
            del self._tasks[task_id]