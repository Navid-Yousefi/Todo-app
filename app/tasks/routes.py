from fastapi import APIRouter



router = APIRouter(tags=['tasks'])



@router.get('/tasks')
def retrive_tasks_list():
    return []


@router.get('/tasks/{task_id}')
def retrive_tasks_detail():
    return []