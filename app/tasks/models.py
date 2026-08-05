from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from core.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    title = Column(String(150), nullable=False)
    description = Column(Text(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship('UserModel', back_populates='tasks', uselist=False)