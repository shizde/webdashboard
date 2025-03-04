import json
from flask import Flask
from flask_jwt_extended import create_access_token
from ..src import create_app, db
from ..src.models.user import User
from ..src.models.expense import Expense


def test_create_expense(client, access_token):
    """
    Test creating a new expense
    """
    expense_data = {
        "amount": 100.50,
        "category": "Groceries",
        "description": "Weekly shopping",
    }

    response = client.post(
        "/expenses",
        data=json.dumps(expense_data),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert response.json["message"] == "Expense created successfully"
    assert response.json["expense"]["amount"] == 100.50
    assert response.json["expense"]["category"] == "Groceries"


def test_get_expenses(client, access_token):
    """
    Test retrieving expenses
    """
    response = client.get(
        "/expenses", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert "expenses" in response.json
    assert "total" in response.json
    assert "pages" in response.json


def test_update_expense(client, access_token, test_expense):
    """
    Test updating an existing expense
    """
    update_data = {"amount": 150.75, "category": "Dining"}

    response = client.put(
        f"/expenses/{test_expense.id}",
        data=json.dumps(update_data),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Expense updated successfully"
    assert response.json["expense"]["amount"] == 150.75
    assert response.json["expense"]["category"] == "Dining"


def test_delete_expense(client, access_token, test_expense):
    """
    Test deleting an expense
    """
    response = client.delete(
        f"/expenses/{test_expense.id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Expense deleted successfully"
