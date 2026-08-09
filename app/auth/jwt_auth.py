from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError, PyJWTError
from core.config import settings
from users.model import UserModel

security = HTTPBearer()

def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        user_id = decoded.get('user_id', None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, user_id not in the payload')
        
        if decoded.get('type') != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, token type not valid')
        
        if datetime.now() > datetime.fromtimestamp(decoded.get("exp")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authetication failed, token expired')
        
        user_obj = db.query(UserModel).filter_by(id=user_id).one_or_none()
        return user_obj

        
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, invalid sinature')

    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, decode failed')

    except PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authentication Failed, {str(e)}')



def generate_access_token(user_id: int, expires_in: int = 60*5):
    now = datetime.now(timezone.utc)
    payload = {
        'type': 'access',
        'user_id': user_id,
        'iat': now,
        'exp': now + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user_id: int, expires_in: int = 3600*24):
    now = datetime.now(timezone.utc)
    payload = {
        'type': 'refresh',
        'user_id': user_id,
        'iat': now,
        'exp': now + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')



def decode_refresh_token(token):

    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms='HS256')
        user_id = decoded.get('user_id', None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, user_id not in the payload')
        
        if decoded.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, token type not valid')
        
        if datetime.now() > datetime.fromtimestamp(decoded.get('exp')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authetication failed, token expired')
        

        return user_id

        
    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, invalid sinature')

    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed, decode failed')

    except PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Authentication Failed, {str(e)}')



