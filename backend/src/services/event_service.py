from sqlalchemy import func
from datetime import datetime, timedelta
from .. import db
from ..models.event import Event


class EventService:
    """
    Service layer for handling complex event-related operations
    """

    @staticmethod
    def get_upcoming_events(user_id, days_ahead=30):
        """
        Retrieve upcoming events for a user

        Args:
            user_id (int): User's unique identifier
            days_ahead (int): Number of days to look ahead

        Returns:
            list: Upcoming events
        """
        current_time = datetime.utcnow()
        end_threshold = current_time + timedelta(days=days_ahead)

        upcoming_events = (
            Event.query.filter(
                Event.user_id == user_id,
                Event.start_time.between(current_time, end_threshold),
            )
            .order_by(Event.start_time.asc())
            .all()
        )

        return [event.to_dict() for event in upcoming_events]

    @staticmethod
    def get_events_by_category(user_id, category):
        """
        Retrieve events for a specific category

        Args:
            user_id (int): User's unique identifier
            category (str): Event category

        Returns:
            list: Events in the specified category
        """
        events = (
            Event.query.filter_by(user_id=user_id, category=category)
            .order_by(Event.start_time.desc())
            .all()
        )

        return [event.to_dict() for event in events]

    @staticmethod
    def create_event(user_id, event_data):
        """
        Create a new event with validation

        Args:
            user_id (int): User's unique identifier
            event_data (dict): Event details

        Returns:
            Event: Created event object
        """
        # Parse datetime strings if they are strings
        start_time = event_data.get("start_time")
        end_time = event_data.get("end_time")

        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)

        # Validate event times
        Event.validate_event(start_time, end_time)

        # Create new event
        new_event = Event(
            user_id=user_id,
            title=event_data.get("title"),
            description=event_data.get("description"),
            start_time=start_time,
            end_time=end_time,
            category=event_data.get("category"),
            location=event_data.get("location"),
        )

        try:
            db.session.add(new_event)
            db.session.commit()
            return new_event
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating event: {str(e)}")

    @staticmethod
    def generate_event_summary(user_id, start_date=None, end_date=None):
        """
        Generate a summary of events for a user

        Args:
            user_id (int): User's unique identifier
            start_date (datetime, optional): Summary start date
            end_date (datetime, optional): Summary end date

        Returns:
            dict: Event summary
        """
        # Default to last 3 months if no dates provided
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=90)
        if not end_date:
            end_date = datetime.utcnow()

        # Total number of events
        total_events = (
            db.session.query(func.count(Event.id))
            .filter(
                Event.user_id == user_id, Event.start_time.between(start_date, end_date)
            )
            .scalar()
        )

        # Events by category
        category_breakdown = (
            db.session.query(Event.category, func.count(Event.id).label("event_count"))
            .filter(
                Event.user_id == user_id, Event.start_time.between(start_date, end_date)
            )
            .group_by(Event.category)
            .all()
        )

        # Busiest days
        busiest_days = (
            db.session.query(
                func.date(Event.start_time).label("event_date"),
                func.count(Event.id).label("event_count"),
            )
            .filter(
                Event.user_id == user_id, Event.start_time.between(start_date, end_date)
            )
            .group_by("event_date")
            .order_by(func.count(Event.id).desc())
            .limit(5)
            .all()
        )

        return {
            "total_events": total_events,
            "start_date": start_date,
            "end_date": end_date,
            "category_breakdown": [
                {"category": category, "event_count": event_count}
                for category, event_count in category_breakdown
            ],
            "busiest_days": [
                {"date": str(event_date), "event_count": event_count}
                for event_date, event_count in busiest_days
            ],
        }

    @staticmethod
    def find_time_conflicts(user_id, start_time, end_time):
        """
        Check for event time conflicts

        Args:
            user_id (int): User's unique identifier
            start_time (datetime): Proposed event start time
            end_time (datetime): Proposed event end time

        Returns:
            list: Conflicting events
        """
        conflicting_events = Event.query.filter(
            Event.user_id == user_id,
            Event.start_time < end_time,
            Event.end_time > start_time,
        ).all()

        return [event.to_dict() for event in conflicting_events]
