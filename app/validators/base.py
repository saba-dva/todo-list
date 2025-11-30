from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

class BaseValidator(ABC):
    """Base validator class"""
    
    @abstractmethod
    def validate(self, value) -> bool:
        pass
    
    def __call__(self, value) -> bool:
        return self.validate(value)