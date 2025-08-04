from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.crud.transaction import create_transaction, get_transactions_by_category
from app.crud.budget import has_budget_write_access
from app.routes.user import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TransactionOut)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    # Find the budget for the category
    from app.models.category import Category
    category = db.query(Category).filter(Category.id == transaction.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    if category.budget_id is not None and not has_budget_write_access(db, category.budget_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to add transactions to this budget.")
    return create_transaction(db, category_id=transaction.category_id, amount=transaction.amount, note=transaction.note)

@router.get("/", response_model=list[TransactionOut])
def list_transactions(db: Session = Depends(get_db), category_id: int = None, current_user=Depends(get_current_user)):
    return get_transactions_by_category(db, category_id=category_id)
