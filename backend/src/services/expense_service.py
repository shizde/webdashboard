from sqlalchemy import func
from datetime import datetime, timedelta
from .. import db
from ..models.expense import Expense


class ExpenseService:
    """
    Service layer for handling complex expense-related operations
    """

    @staticmethod
    def calculate_monthly_spending(user_id, months=3):
        """
        Calculate monthly spending for a given user

        Args:
            user_id (int): User's unique identifier
            months (int): Number of recent months to analyze

        Returns:
            list: Monthly spending data
        """
        # Calculate the date threshold
        threshold_date = datetime.utcnow() - timedelta(days=months * 30)

        monthly_spending = (
            db.session.query(
                func.date_trunc("month", Expense.date).label("month"),
                func.sum(Expense.amount).label("total_amount"),
            )
            .filter(Expense.user_id == user_id, Expense.date >= threshold_date)
            .group_by("month")
            .order_by("month")
            .all()
        )

        return [
            {"month": month.strftime("%Y-%m"), "total_amount": float(amount)}
            for month, amount in monthly_spending
        ]

    @staticmethod
    def get_top_expenses_by_category(user_id, limit=5):
        """
        Get top expenses grouped by category

        Args:
            user_id (int): User's unique identifier
            limit (int): Number of top categories to return

        Returns:
            list: Top expense categories
        """
        top_categories = (
            db.session.query(
                Expense.category, func.sum(Expense.amount).label("total_amount")
            )
            .filter(Expense.user_id == user_id)
            .group_by(Expense.category)
            .order_by(func.sum(Expense.amount).desc())
            .limit(limit)
            .all()
        )

        return [
            {"category": category, "total_amount": float(amount)}
            for category, amount in top_categories
        ]

    @staticmethod
    def predict_next_month_expenses(user_id):
        """
        Predict next month's expenses based on historical data

        Args:
            user_id (int): User's unique identifier

        Returns:
            dict: Predicted expenses
        """
        # Get average monthly spending for the last 3 months
        threshold_date = datetime.utcnow() - timedelta(days=90)

        monthly_averages = (
            db.session.query(
                Expense.category, func.avg(Expense.amount).label("avg_amount")
            )
            .filter(Expense.user_id == user_id, Expense.date >= threshold_date)
            .group_by(Expense.category)
            .all()
        )

        return {
            category: float(avg_amount) for category, avg_amount in monthly_averages
        }

    @staticmethod
    def add_expense(user_id, amount, category, description=None, date=None):
        """
        Add a new expense with validation

        Args:
            user_id (int): User's unique identifier
            amount (float): Expense amount
            category (str): Expense category
            description (str, optional): Expense description
            date (datetime, optional): Expense date

        Returns:
            Expense: Created expense object
        """
        # Validate expense
        Expense.validate_expense(amount, category)

        # Create expense
        new_expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=date or datetime.utcnow(),
        )

        try:
            db.session.add(new_expense)
            db.session.commit()
            return new_expense
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating expense: {str(e)}")

    @staticmethod
    def generate_expense_report(user_id, start_date=None, end_date=None):
        """
        Generate a comprehensive expense report

        Args:
            user_id (int): User's unique identifier
            start_date (datetime, optional): Report start date
            end_date (datetime, optional): Report end date

        Returns:
            dict: Comprehensive expense report
        """
        # Default to last 3 months if no dates provided
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=90)
        if not end_date:
            end_date = datetime.utcnow()

        # Total spending
        total_spending = (
            db.session.query(func.sum(Expense.amount))
            .filter(
                Expense.user_id == user_id, Expense.date.between(start_date, end_date)
            )
            .scalar()
            or 0.0
        )

        # Category breakdown
        category_breakdown = (
            db.session.query(
                Expense.category,
                func.sum(Expense.amount).label("total_amount"),
                func.count(Expense.id).label("transaction_count"),
            )
            .filter(
                Expense.user_id == user_id, Expense.date.between(start_date, end_date)
            )
            .group_by(Expense.category)
            .all()
        )

        return {
            "total_spending": float(total_spending),
            "start_date": start_date,
            "end_date": end_date,
            "category_breakdown": [
                {
                    "category": category,
                    "total_amount": float(total_amount),
                    "transaction_count": transaction_count,
                }
                for category, total_amount, transaction_count in category_breakdown
            ],
        }
