from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.category import CategoryCreate, CategoryOut
from app.crud.category import create_category, get_categories_by_budget
from app.crud.budget import has_budget_write_access
from app.routes.user import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryOut)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not has_budget_write_access(db, category.budget_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to add categories to this budget.")
    return create_category(db, budget_id=category.budget_id, name=category.name)

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), budget_id: int = None, current_user=Depends(get_current_user)):
    return get_categories_by_budget(db, budget_id=budget_id)
