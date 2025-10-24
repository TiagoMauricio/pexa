from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.users import UserCreate, User as UserResponse
from typing import List
import app.crud.users as user_crud

router = APIRouter()


@router.post("", response_model=UserResponse)
async def create_user_endpoint(
    user_data: UserCreate, session: Session = Depends(get_session)
):
    """Create a new user"""

    # Check if user with this email already exists
    existing_user = user_crud.find_user_by_email(user_data.email, session)

    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    # Create new user
    new_user = user_crud.create_user(user_data, session)
    return new_user


@router.get("", response_model=List[UserResponse])
async def get_all_users(session: Session = Depends(get_session)):
    """Fetch all users"""

    users = user_crud.find_all_users(session)
    return users
