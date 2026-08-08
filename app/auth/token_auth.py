from fastapi import HTTPException,status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.database import get_db
from sqlalchemy.orm import Session
from users.model import UserModel, TokenModel


security = HTTPBearer(scheme_name='Token')


def get_authenticated_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    token_obj = db.query(TokenModel).filter_by(token=credentials.credentials).one_or_none()
    if not token_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authetication Failde'
        )

    #other logic


    return token_obj.user