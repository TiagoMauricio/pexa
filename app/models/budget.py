from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.encryption import encrypt_field, decrypt_field

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    name_encrypted = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="budgets")
    categories = relationship("Category", back_populates="budget")
    shares = relationship("BudgetShare", back_populates="budget")

    @property
    def name(self):
        return decrypt_field(self.name_encrypted)

    @name.setter
    def name(self, value):
        self.name_encrypted = encrypt_field(value)

class BudgetShare(Base):
    __tablename__ = "budget_shares"
    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    can_write = Column(Boolean, default=False)
    budget = relationship("Budget", back_populates="shares")
    user = relationship("User", back_populates="shared_budgets")
