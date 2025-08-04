from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.encryption import encrypt_field, decrypt_field

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount_encrypted = Column(String, nullable=False)
    note_encrypted = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="transactions")

    @property
    def amount(self):
        return float(decrypt_field(self.amount_encrypted))

    @amount.setter
    def amount(self, value):
        self.amount_encrypted = encrypt_field(str(value))

    @property
    def note(self):
        return decrypt_field(self.note_encrypted) if self.note_encrypted else None

    @note.setter
    def note(self, value):
        self.note_encrypted = encrypt_field(value) if value else None
