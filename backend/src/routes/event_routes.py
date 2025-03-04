from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
from .. import db
from ..models.event import Event

# Create event blueprint
event_bp = Blueprint("events", __name__)


@event_bp.route("", methods=["POST"])
@jwt_required()
def create_event():
    """
    Create a new event
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Validate input
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Parse datetime strings
        start_time = datetime.fromisoformat(data.get("start_time"))
        end_time = datetime.fromisoformat(data.get("end_time"))

        # Validate event times
        Event.validate_event(start_time, end_time)

        # Create new event
        new_event = Event(
            user_id=current_user_id,
            title=data.get("title"),
            description=data.get("description"),
            start_time=start_time,
            end_time=end_time,
            category=data.get("category"),
            location=data.get("location"),
        )

        db.session.add(new_event)
        db.session.commit()

        return jsonify(
            {"message": "Event created successfully", "event": new_event.to_dict()}
        ), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@event_bp.route("", methods=["GET"])
@jwt_required()
def get_events():
    """
    Retrieve events for the current user
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
    query = Event.query.filter_by(user_id=current_user_id)

    # Apply filters
    if category:
        query = query.filter(Event.category == category)

    if start_date:
        query = query.filter(Event.start_time >= start_date)

    if end_date:
        query = query.filter(Event.end_time <= end_date)

    # Paginate results
    paginated_events = query.order_by(Event.start_time.asc()).paginate(
        page=page, per_page=per_page
    )

    return jsonify(
        {
            "events": [event.to_dict() for event in paginated_events.items],
            "total": paginated_events.total,
            "pages": paginated_events.pages,
            "current_page": page,
        }
    ), 200


@event_bp.route("/upcoming", methods=["GET"])
@jwt_required()
def get_upcoming_events():
    """
    Get upcoming events for the current user
    """
    current_user_id = get_jwt_identity()
    current_time = datetime.utcnow()

    # Query upcoming events sorted by start time
    upcoming_events = (
        Event.query.filter(
            Event.user_id == current_user_id, Event.start_time > current_time
        )
        .order_by(Event.start_time.asc())
        .limit(10)
        .all()
    )

    return jsonify(
        {"upcoming_events": [event.to_dict() for event in upcoming_events]}
    ), 200


@event_bp.route("/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    """
    Update an existing event
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Find the event
    event = Event.query.filter_by(id=event_id, user_id=current_user_id).first()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        # Update event fields
        if "title" in data:
            event.title = data["title"]

        if "description" in data:
            event.description = data["description"]

        if "start_time" in data and "end_time" in data:
            start_time = datetime.fromisoformat(data["start_time"])
            end_time = datetime.fromisoformat(data["end_time"])
            Event.validate_event(start_time, end_time)
            event.start_time = start_time
            event.end_time = end_time

        if "category" in data:
            event.category = data["category"]

        if "location" in data:
            event.location = data["location"]

        db.session.commit()

        return jsonify(
            {"message": "Event updated successfully", "event": event.to_dict()}
        ), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@event_bp.route("/<int:event_id>", methods=["DELETE"])
@jwt_required()
def delete_event(event_id):
    """
    Delete an existing event
    """
    current_user_id = get_jwt_identity()

    # Find the event
    event = Event.query.filter_by(id=event_id, user_id=current_user_id).first()

    if not event:
        return jsonify({"error": "Event not found"}), 404

    try:
        db.session.delete(event)
        db.session.commit()

        return jsonify({"message": "Event deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
