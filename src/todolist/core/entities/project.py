from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Project:
    id: str
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    
    def update(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        self.updated_at = datetime.now()