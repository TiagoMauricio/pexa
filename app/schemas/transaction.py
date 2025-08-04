from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    amount: float
    note: Optional[str] = None

class TransactionCreate(TransactionBase):
    category_id: int

class TransactionOut(TransactionBase):
    id: int
    category_id: int
    class Config:
        orm_mode = True
