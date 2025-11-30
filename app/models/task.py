from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Task:
    id: str
    project_id: str
    title: str
    description: str
    status: TaskStatus
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    def update_status(self, status: TaskStatus) -> None:
        self.status = status
        self.updated_at = datetime.now()
    
    def update_details(self, title: str, description: str, deadline: Optional[datetime]) -> None:
        self.title = title
        self.description = description
        self.deadline = deadline
        self.updated_at = datetime.now()