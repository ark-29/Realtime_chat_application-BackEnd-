from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

Key = "<Your Key>"
Algorithm = "HS256"
token_expire_time = 60 * 24 * 30

oAuth = OAuth2PasswordBearer(tokenUrl="/login")

def create_token(data: dict, expires_delta: int = token_expire_time):
    data_copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    data_copy.update({"expire": expire.timestamp()})
    created_token = jwt.encode(data_copy, Key, algorithm=Algorithm)
    return created_token

def verify_token(token: str = Depends(oAuth)):
    try:
        payload = jwt.decode(token, Key, algorithms=[Algorithm])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

