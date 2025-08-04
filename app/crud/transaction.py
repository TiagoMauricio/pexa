from sqlalchemy.orm import Session
from app.models.transaction import Transaction

def create_transaction(db: Session, category_id: int, amount: float, note: str = None):
    transaction = Transaction(category_id=category_id)
    transaction.amount = amount
    transaction.note = note
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transactions_by_category(db: Session, category_id: int):
    return db.query(Transaction).filter(Transaction.category_id == category_id).all()
