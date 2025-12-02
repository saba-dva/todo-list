from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db_session: Session):
        self.model = model
        self.db_session = db_session
    
    def get(self, id: int) -> Optional[ModelType]:
        return self.db_session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self) -> List[ModelType]:
        return self.db_session.query(self.model).all()
    
    def create(self, obj: ModelType) -> ModelType:
        self.db_session.add(obj)
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj
    
    def update(self, obj: ModelType) -> ModelType:
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj
    
    def delete(self, id: int) -> None:
        obj = self.get(id)
        if obj:
            self.db_session.delete(obj)
            self.db_session.commit()