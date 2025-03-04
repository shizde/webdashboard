from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class User(db.Model):
    """
    User model for storing user account information
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    expenses = relationship(
        "Expense", back_populates="user", cascade="all, delete-orphan"
    )
    events = relationship("Event", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        """
        Create hashed password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check hashed password
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Serialize user object to dictionary
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        """
        String representation of the User model
        """
        return f"<User {self.username}>"
