from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from core.database import Base
from datetime import datetime



class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', is_completed={self.is_completed})>"
