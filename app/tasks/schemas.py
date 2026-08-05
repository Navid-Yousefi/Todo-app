from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=100, min_length=5, description='Task title')
    description: Optional[str] = Field(None, max_length=500, description='Task description')
    is_completed: bool = Field(False, description='Task completion status')


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=100, min_length=5, description='Task title')
    description: Optional[str] = Field(None, max_length=500, description='Task description')
    is_completed: Optional[bool] = Field(None, description='Task completion status')


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description='Task ID')
    created_at: datetime = Field(..., description='Task creation timestamp')
    updated_at: datetime = Field(..., description='Task last update timestamp')