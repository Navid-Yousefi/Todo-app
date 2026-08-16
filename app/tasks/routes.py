from fastapi import APIRouter, status, Depends, Query, HTTPException
from tasks.schemas import (
    TaskCreateSchema,
    TaskResponseSchema,
    TaskUpdateSchema,
)
from typing import List
from sqlalchemy.orm import Session
from core.database import get_db
from tasks.models import TaskModel
from fastapi.responses import JSONResponse
from auth.jwt_auth import get_authenticated_user
from users.model import UserModel

router = APIRouter(tags=["tasks"], prefix="/tasks")


@router.get(
    "/tasks-list",
    status_code=status.HTTP_200_OK,
    response_model=List[TaskResponseSchema],
)
def retrive_tasks_list(
    is_completed: bool = Query(
        None, description="Filter tasks by completion status or not"
    ),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = db.query(TaskModel).filter_by(user_id=user.id)
    if is_completed is not None:
        query = query.filter_by(is_completed=is_completed)
    return query.all()


@router.get(
    "/detail", status_code=status.HTTP_200_OK, response_model=TaskResponseSchema
)
def retrive_tasks_detail(
    task_id: int = Query(...),
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    query = (
        db.query(TaskModel)
        .filter_by(user_id=user.id, id=task_id)
        .one_or_none()
    )

    if query:
        return query

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
    )


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponseSchema,
)
def create_tast(
    request: TaskCreateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    task_obj = TaskModel(**data)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.patch(
    "/tast-update",
    status_code=status.HTTP_200_OK,
    response_model=TaskResponseSchema,
)
def update_task(
    task_id: int,
    request: TaskUpdateSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = (
        db.query(TaskModel)
        .filter_by(user_id=user.id, id=task_id)
        .one_or_none()
    )

    if task_obj is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task_obj, key, value)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.delete("/delete-task/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    task_obj = (
        db.query(TaskModel)
        .filter_by(user_id=user.id, id=task_id)
        .one_or_none()
    )
    if task_obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    db.delete(task_obj)
    db.commit()
    return JSONResponse(
        content={"message": "Task deleted successfully"},
        status_code=status.HTTP_200_OK,
    )
