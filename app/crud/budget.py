from sqlalchemy.orm import Session
from app.models.budget import Budget, BudgetShare

def create_budget(db: Session, owner_id: int, name: str):
    budget = Budget(owner_id=owner_id)
    budget.name = name
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget

def get_budgets_by_user(db: Session, user_id: int):
    return db.query(Budget).filter(Budget.owner_id == user_id).all()

def get_accessible_budgets(db: Session, user_id: int):
    """Return all budgets a user owns or is shared with."""
    owned = db.query(Budget).filter(Budget.owner_id == user_id)
    shared = db.query(Budget).join(BudgetShare).filter(BudgetShare.user_id == user_id)
    return list(set(owned).union(shared))

def has_budget_write_access(db: Session, budget_id: int, user_id: int) -> bool:
    """Return True if user is owner or has can_write access to the budget."""
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        return False
    if budget.owner_id == user_id:
        return True
    share = db.query(BudgetShare).filter_by(budget_id=budget_id, user_id=user_id).first()
    return bool(share and share.can_write)

def share_budget(db: Session, budget_id: int, user_id: int, can_write: bool = False):
    share = BudgetShare(budget_id=budget_id, user_id=user_id, can_write=can_write)
    db.add(share)
    db.commit()
    db.refresh(share)
    return share
