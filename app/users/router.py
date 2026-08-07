from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from core.database import get_db
from sqlalchemy.orm import Session
from users.schemas import *
from users.model import UserModel
from fastapi.responses import JSONResponse

router = APIRouter(tags=['users'], prefix='/users')


@router.post('/login')
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username = request.username).first
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user denst exists')
    if not user_obj.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='password is invalid')
    return {}


@router.post('/register')
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username = request.username.lower).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='username alredy exists')

    user_obj = UserModel(username=request.username.lower, email=request.email)
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    # db.refresh(user_obj)
    return JSONResponse(content={'detail': 'user registered succsassfully'})