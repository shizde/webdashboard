from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .. import db
from .user import User


class Event(db.Model):
    """
    Event model for tracking user calendar events
    """

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    category = Column(String(50))
    location = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="events")

    def to_dict(self):
        """
        Serialize event object to dictionary
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "category": self.category,
            "location": self.location,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def validate_event(cls, start_time, end_time):
        """
        Validate event time constraints
        """
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")

    def __repr__(self):
        """
        String representation of the Event model
        """
        return f"<Event {self.id}: {self.title} - {self.start_time}>"
