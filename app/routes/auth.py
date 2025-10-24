from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.database import get_session
import app.crud.users as user_crud
from app.schemas.users import UserCreate, User as UserResponse
from app.schemas.token import Token
from app.utils.security import (
    verify_password,
    create_access_token,
)

router = APIRouter(tags=["authentication"])


def authenticate_user(email: str, password: str, session: Session):
    user = user_crud.find_user_by_email(email, session)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate, session: Session = Depends(get_session)
) -> UserResponse:
    """Register a new user."""
    # Check if user with this email already exists
    existing_user = user_crud.find_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    # Create new user
    # TODO: return 400 if password is not ok
    new_user = user_crud.create_user(user_data, session)

    # TODO: Send verification email

    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """
    OAuth2 compatible token login, get an access token for future requests.

    - **username**: The user's email
    - **password**: The user's password
    """
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
