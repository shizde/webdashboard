import pytest
from datetime import datetime, timedelta
from ..src import create_app, db
from ..src.models.user import User
from ..src.models.expense import Expense
from ..src.models.event import Event
from flask_jwt_extended import create_access_token


@pytest.fixture(scope="session")
def app():
    """
    Create a Flask app for testing
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    """
    Create a test client
    """
    return app.test_client()


@pytest.fixture(scope="function")
def test_user(app):
    """
    Create a test user for each test function
    """
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture(scope="function")
def access_token(test_user):
    """
    Generate an access token for the test user
    """
    return create_access_token(identity=test_user.id)


@pytest.fixture(scope="function")
def test_expense(test_user):
    """
    Create a test expense for each test function
    """
    with db.session.begin():
        expense = Expense(
            user_id=test_user.id,
            amount=100.00,
            category="Test Category",
            description="Test Expense",
        )
        db.session.add(expense)

    return expense


@pytest.fixture(scope="function")
def test_event(test_user):
    """
    Create a test event for each test function
    """
    with db.session.begin():
        event = Event(
            user_id=test_user.id,
            title="Test Event",
            start_time=datetime.utcnow() + timedelta(days=1),
            end_time=datetime.utcnow() + timedelta(days=1, hours=2),
            category="Test Category",
        )
        db.session.add(event)

    return event
