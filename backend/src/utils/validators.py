import re
from email_validator import validate_email as email_validate, EmailNotValidError


def validate_email(email):
    """
    Validate email address

    Args:
        email (str): Email address to validate

    Returns:
        str: Normalized email address

    Raises:
        ValueError: If email is invalid
    """
    try:
        # Validate and get normalized email
        valid = email_validate(email)
        return valid.email
    except EmailNotValidError as e:
        raise ValueError(f"Invalid email address: {str(e)}")


def validate_password(password):
    """
    Validate password strength

    Args:
        password (str): Password to validate

    Raises:
        ValueError: If password does not meet requirements
    """
    # Check minimum length
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")

    # Check for at least one digit
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one number")

    # Check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain at least one special character")


def validate_username(username):
    """
    Validate username

    Args:
        username (str): Username to validate

    Returns:
        str: Validated username

    Raises:
        ValueError: If username is invalid
    """
    # Check username length
    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long")

    if len(username) > 50:
        raise ValueError("Username must be no more than 50 characters long")

    # Check for valid characters (alphanumeric and underscore)
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        raise ValueError("Username can only contain letters, numbers, and underscores")

    return username


def validate_expense_data(amount, category):
    """
    Validate expense data

    Args:
        amount (float): Expense amount
        category (str): Expense category

    Raises:
        ValueError: If data is invalid
    """
    # Validate amount
    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")

    if amount <= 0:
        raise ValueError("Amount must be a positive number")

    # Validate category
    if not category or not isinstance(category, str):
        raise ValueError("Category must be a non-empty string")

    if len(category) > 50:
        raise ValueError("Category must be 50 characters or less")


def validate_event_data(title, start_time, end_time):
    """
    Validate event data

    Args:
        title (str): Event title
        start_time (datetime): Event start time
        end_time (datetime): Event end time

    Raises:
        ValueError: If data is invalid
    """
    # Validate title
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")

    if len(title) > 100:
        raise ValueError("Title must be 100 characters or less")

    # Validate time
    if start_time >= end_time:
        raise ValueError("Start time must be before end time")
