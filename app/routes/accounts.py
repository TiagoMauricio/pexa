from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models import Account
from app.schemas.accounts import AccountCreate, Account as AccountResponse
import app.crud.account as account_crud
from typing import List

router = APIRouter()

@router.get("", response_model=List[AccountResponse])
async def get_all_accounts(session: Session = Depends(get_session)):
    accounts = account_crud.get_all_accounts(session)
    return accounts

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account_by_id(account_id: int, session: Session = Depends(get_session)):
    account = account_crud.get_account_by_id(account_id, session)
    return account

@router.post("")
async def create_account_endpoint(
    account_data: AccountCreate,
    session: Session = Depends(get_session)
):
    new_account = account_crud.create_account(account_data, session)
    return new_account
