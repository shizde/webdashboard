from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from .. import db
from ..models.expense import Expense
from ..models.user import User

# Create expense blueprint
expense_bp = Blueprint("expenses", __name__)


@expense_bp.route("", methods=["POST"])
@jwt_required()
def create_expense():
    """
    Create a new expense
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Validate expense data
        Expense.validate_expense(data.get("amount"), data.get("category"))

        # Create new expense
        new_expense = Expense(
            user_id=current_user_id,
            amount=data.get("amount"),
            category=data.get("category"),
            description=data.get("description"),
        )

        db.session.add(new_expense)
        db.session.commit()

        return jsonify(
            {
                "message": "Expense created successfully",
                "expense": new_expense.to_dict(),
            }
        ), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@expense_bp.route("", methods=["GET"])
@jwt_required()
def get_expenses():
    """
    Retrieve expenses for the current user
    Support filtering and pagination
    """
    current_user_id = get_jwt_identity()

    # Get query parameters
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Base query
    query = Expense.query.filter_by(user_id=current_user_id)

    # Apply filters
    if category:
        query = query.filter(Expense.category == category)

    if start_date:
        query = query.filter(Expense.date >= start_date)

    if end_date:
        query = query.filter(Expense.date <= end_date)

    # Paginate results
    paginated_expenses = query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
        {
            "expenses": [expense.to_dict() for expense in paginated_expenses.items],
            "total": paginated_expenses.total,
            "pages": paginated_expenses.pages,
            "current_page": page,
        }
    ), 200


@expense_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_expense_summary():
    """
    Get expense summary statistics
    """
    current_user_id = get_jwt_identity()

    # Total expenses by category
    category_summary = (
        db.session.query(
            Expense.category, func.sum(Expense.amount).label("total_amount")
        )
        .filter(Expense.user_id == current_user_id)
        .group_by(Expense.category)
        .all()
    )

    # Monthly total expenses
    monthly_summary = (
        db.session.query(
            func.date_trunc("month", Expense.date).label("month"),
            func.sum(Expense.amount).label("total_amount"),
        )
        .filter(Expense.user_id == current_user_id)
        .group_by("month")
        .order_by("month")
        .all()
    )

    return jsonify(
        {
            "category_summary": [
                {"category": cat, "total_amount": float(amount)}
                for cat, amount in category_summary
            ],
            "monthly_summary": [
                {"month": str(month), "total_amount": float(amount)}
                for month, amount in monthly_summary
            ],
        }
    ), 200


@expense_bp.route("/<int:expense_id>", methods=["PUT"])
@jwt_required()
def update_expense(expense_id):
    """
    Update an existing expense
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Find the expense
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    try:
        # Update expense fields
        if "amount" in data:
            Expense.validate_expense(data["amount"], expense.category)
            expense.amount = data["amount"]

        if "category" in data:
            Expense.validate_expense(expense.amount, data["category"])
            expense.category = data["category"]

        if "description" in data:
            expense.description = data["description"]

        db.session.commit()

        return jsonify(
            {"message": "Expense updated successfully", "expense": expense.to_dict()}
        ), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@expense_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    """
    Delete an existing expense
    """
    current_user_id = get_jwt_identity()

    # Find the expense
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user_id).first()

    if not expense:
        return jsonify({"error": "Expense not found"}), 404

    try:
        db.session.delete(expense)
        db.session.commit()

        return jsonify({"message": "Expense deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
