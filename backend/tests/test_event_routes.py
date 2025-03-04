import json
from datetime import datetime, timedelta
from flask import Flask
from flask_jwt_extended import create_access_token
from ..src import create_app, db
from ..src.models.user import User
from ..src.models.event import Event


def test_create_event(client, access_token):
    """
    Test creating a new event
    """
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    event_data = {
        "title": "Team Meeting",
        "description": "Quarterly review",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "category": "Work",
        "location": "Conference Room",
    }

    response = client.post(
        "/events",
        data=json.dumps(event_data),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201
    assert response.json["message"] == "Event created successfully"
    assert response.json["event"]["title"] == "Team Meeting"


def test_get_events(client, access_token):
    """
    Test retrieving events
    """
    response = client.get(
        "/events", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert "events" in response.json
    assert "total" in response.json
    assert "pages" in response.json


def test_get_upcoming_events(client, access_token):
    """
    Test retrieving upcoming events
    """
    response = client.get(
        "/events/upcoming", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert "upcoming_events" in response.json


def test_update_event(client, access_token, test_event):
    """
    Test updating an existing event
    """
    start_time = datetime.utcnow() + timedelta(days=2)
    end_time = start_time + timedelta(hours=3)

    update_data = {
        "title": "Updated Team Meeting",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
    }

    response = client.put(
        f"/events/{test_event.id}",
        data=json.dumps(update_data),
        content_type="application/json",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Event updated successfully"
    assert response.json["event"]["title"] == "Updated Team Meeting"


def test_delete_event(client, access_token, test_event):
    """
    Test deleting an event
    """
    response = client.delete(
        f"/events/{test_event.id}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "Event deleted successfully"
