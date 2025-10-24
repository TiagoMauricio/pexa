from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.database import get_session
import app.crud.users as user_crud
from app.schemas.users import UserCreate, User as UserResponse

router = APIRouter(tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
) -> UserResponse:
    """Register a new user."""
    # Check if user with this email already exists
    existing_user = user_crud.find_user_by_email(user_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    # TODO: return 400 if password is not ok
    new_user = user_crud.create_user(user_data, session)

    # TODO: Send verification email

    return new_user
