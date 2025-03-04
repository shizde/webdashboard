from datetime import datetime, timedelta
from ..src.services.expense_service import ExpenseService
from ..src.services.event_service import EventService
from ..src.models.user import User


def test_expense_monthly_spending(test_user):
    """
    Test calculate monthly spending service
    """
    # Add some test expenses
    expenses = [
        {"amount": 100, "category": "Groceries", "date": datetime.utcnow()},
        {
            "amount": 50,
            "category": "Dining",
            "date": datetime.utcnow() - timedelta(days=30),
        },
        {
            "amount": 200,
            "category": "Entertainment",
            "date": datetime.utcnow() - timedelta(days=60),
        },
    ]

    for expense_data in expenses:
        ExpenseService.add_expense(
            user_id=test_user.id,
            amount=expense_data["amount"],
            category=expense_data["category"],
            date=expense_data["date"],
        )

    monthly_spending = ExpenseService.calculate_monthly_spending(test_user.id)

    assert len(monthly_spending) > 0
    assert all("month" in item and "total_amount" in item for item in monthly_spending)


def test_event_upcoming_events(test_user):
    """
    Test get upcoming events service
    """
    start_time = datetime.utcnow() + timedelta(days=1)
    events = [
        {
            "title": f"Event {i}",
            "start_time": start_time + timedelta(days=i),
            "end_time": start_time + timedelta(days=i, hours=2),
            "category": "Work",
        }
        for i in range(3)
    ]

    for event_data in events:
        EventService.create_event(user_id=test_user.id, event_data=event_data)

    upcoming_events = EventService.get_upcoming_events(test_user.id)

    assert len(upcoming_events) == 3
    assert all("id" in event and "title" in event for event in upcoming_events)


def test_event_summary(test_user):
    """
    Test event summary generation
    """
    start_time = datetime.utcnow() - timedelta(days=90)
    events = [
        {
            "title": f"Event {i}",
            "start_time": start_time + timedelta(days=i * 10),
            "end_time": start_time + timedelta(days=i * 10, hours=2),
            "category": "Work" if i % 2 == 0 else "Personal",
        }
        for i in range(10)
    ]

    for event_data in events:
        EventService.create_event(user_id=test_user.id, event_data=event_data)

    summary = EventService.generate_event_summary(test_user.id)

    assert "total_events" in summary
    assert "category_breakdown" in summary
    assert "busiest_days" in summary
