from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.users import User as UserResponse
from typing import List
import app.crud.users as user_crud

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def get_all_users(session: Session = Depends(get_session)):
    """Fetch all users"""

    users = user_crud.find_all_users(session)
    return users
