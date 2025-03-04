from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db
from .user import User


class Expense(db.Model):
    """
    Expense model for tracking user expenses
    """

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(255))
    date = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="expenses")

    def to_dict(self):
        """
        Serialize expense object to dictionary
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date.isoformat() if self.date else None,
        }

    @classmethod
    def validate_expense(cls, amount, category):
        """
        Validate expense data before creation
        """
        if amount <= 0:
            raise ValueError("Expense amount must be positive")

        if not category or len(category.strip()) == 0:
            raise ValueError("Category cannot be empty")

    def __repr__(self):
        """
        String representation of the Expense model
        """
        return f"<Expense {self.id}: ${self.amount} - {self.category}>"
