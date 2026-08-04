from pydantic import BaseModel, Field
from typing import Optional


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=100, min_length=5, description='Task title')
    description: Optional[str] = Field(None, max_length=500, description='Task description')
    is_completed: bool = Field(False, description='Task completion status')



class TaskCreateSchema(TaskBaseSchema):
    pass



class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: int = Field(..., description='Task ID')
    created_at: str = Field(..., description='Task creation timestamp')
    updated_at: str = Field(..., description='Task last update timestamp')

    class Config:
        orm_mode = True