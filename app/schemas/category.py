from pydantic import BaseModel
from typing import List, Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    budget_id: int

class CategoryOut(CategoryBase):
    id: int
    budget_id: int
    class Config:
        orm_mode = True
