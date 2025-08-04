from sqlalchemy.orm import Session
from app.models.category import Category

def create_category(db: Session, budget_id: int, name: str):
    category = Category(budget_id=budget_id)
    category.name = name
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories_by_budget(db: Session, budget_id: int):
    return db.query(Category).filter(Category.budget_id == budget_id).all()
