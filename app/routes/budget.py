from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.budget import BudgetCreate, BudgetOut, BudgetShareOut
from app.crud.budget import create_budget, get_accessible_budgets, share_budget
from app.routes.user import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BudgetOut)
def create_new_budget(budget: BudgetCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_budget(db, owner_id=current_user.id, name=budget.name)

@router.get("/", response_model=list[BudgetOut])
def list_budgets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_accessible_budgets(db, user_id=current_user.id)

@router.post("/share", response_model=BudgetShareOut)
def share(db: Session = Depends(get_db), budget_id: int = None, user_id: int = None, can_write: bool = False, current_user=Depends(get_current_user)):
    # Only owner can share
    share_obj = share_budget(db, budget_id=budget_id, user_id=user_id, can_write=can_write)
    return BudgetShareOut.from_orm(share_obj)
