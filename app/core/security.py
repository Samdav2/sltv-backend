from datetime import datetime, timedelta
from typing import Any, Union
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: str | Any, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_email_token(email: str, type: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"exp": expire, "sub": email, "type": type}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_email_token(token: str, type: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        email = payload.get("sub")
        if token_type != type or not email:
            return None
        return email
    except JWTError:
        return None

import hashlib

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Pre-hash with SHA256 to support passwords > 72 bytes
    password_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(password_hash, hashed_password)

def get_password_hash(password: str) -> str:
    # Pre-hash with SHA256 to support passwords > 72 bytes
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(password_hash)
