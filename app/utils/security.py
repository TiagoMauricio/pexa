from datetime import datetime, timedelta, timezone
from typing import Dict, Any

import jwt
from fastapi import HTTPException, status
from argon2 import PasswordHasher, exceptions

from app.config import settings

# Initialize Argon2 password hasher
ph = PasswordHasher(
    time_cost=3,          # Number of iterations
    memory_cost=65536,    # 64MB
    parallelism=4,        # Number of parallel threads
    hash_len=32,          # Hash length
    salt_len=16           # Salt length
)

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a password using Argon2"""
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using Argon2"""
    try:
        return ph.verify(hashed_password, plain_password)
    except (exceptions.VerifyMismatchError, exceptions.InvalidHash):
        return False
    except exceptions.VerificationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during password verification"
        )


def create_access_token(data: Dict[str, Any]) -> str:
    """Create a new JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def verify_token(token: str) -> Dict[str, Any]:
    """Verify JWT token and return its payload"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception
