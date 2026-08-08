from fastapi import HTTPException,status, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from core.database import get_db
from sqlalchemy.orm import Session
from users.model import UserModel


security = HTTPBasic()


def get_authenticated_user(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    user_ubj = db.query(UserModel).filter_by(username=credentials.username).one_or_none()
    if not user_ubj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Baseic'}
        )
    if not user_ubj.verify_password(credentials.password):
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Baseic'}
                )
    return user_ubj

