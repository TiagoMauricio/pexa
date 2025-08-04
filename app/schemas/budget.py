from pydantic import BaseModel
from typing import List, Optional

class BudgetBase(BaseModel):
    name: str

class BudgetCreate(BudgetBase):
    pass

class BudgetOut(BudgetBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

from pydantic import ConfigDict

class BudgetShareOut(BaseModel):
    id: int
    user_id: int
    can_write: bool
    model_config = ConfigDict(from_attributes=True)
