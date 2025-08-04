"""
Global base categories initializer.
Creates default categories (e.g., Groceries, Rent, etc.) with no budget_id (global) if not present.
Call from FastAPI startup event.
"""
from app.models.category import Category
from app.utils.encryption import encrypt_field
from sqlalchemy.orm import Session

def get_global_base_category_names():
    return [
        "Groceries",
        "Rent",
        "Utilities",
        "Transportation",
        "Healthcare",
        "Insurance",
        "Dining Out",
        "Entertainment",
        "Savings",
        "Personal Care",
        "Education",
        "Gifts",
        "Travel",
        "Miscellaneous",
    ]

def ensure_global_base_categories(db: Session):
    """
    Idempotently create global base categories if they do not exist (budget_id is None).
    This will not create duplicates on repeated calls.
    """
    names = get_global_base_category_names()
    for name in names:
        encrypted_name = encrypt_field(name)
        exists = db.query(Category).filter_by(budget_id=None, name_encrypted=encrypted_name).first()
        if not exists:
            cat = Category(name_encrypted=encrypted_name, budget_id=None)
            db.add(cat)
    db.commit()
