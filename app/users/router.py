from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from core.database import get_db
from sqlalchemy.orm import Session
from users.schemas import *
from users.model import UserModel, TokenModel
from fastapi.responses import JSONResponse
import secrets
from auth.jwt_auth import (
    generate_access_token,
    generate_refresh_token,
    decode_refresh_token,
)

router = APIRouter(tags=["users"], prefix="/users")


# def generate_toke(length=32):
#     return secrets.token_hex(length)


@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )

    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token_obj = TokenModel(
        user_id=user_obj.id, token=generate_access_token(user_id=user_obj.id)
    )
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "logged in successfulay",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/register")
async def user_register(
    request: UserRegisterSchema, db: Session = Depends(get_db)
):
    if (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username alredy exists",
        )

    user_obj = UserModel(
        username=request.username.lower(), email=request.email
    )
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    # db.refresh(user_obj)
    return JSONResponse(content={"detail": "user registered succsassfully"})


@router.post("/refresh-token")
async def user_refresh_token(
    request: UserRefreshTokenSchama, db: Session = Depends(get_db)
):
    user_id = decode_refresh_token(request.refresh_token)
    access_token = generate_access_token(user_id)
    return JSONResponse(content={"access-token": access_token})
