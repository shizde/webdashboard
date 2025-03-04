from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .. import db
from ..models.user import User

# Create authentication blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    User registration endpoint
    """
    data = request.get_json()

    # Validate input
    if (
        not data
        or not data.get("username")
        or not data.get("email")
        or not data.get("password")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == data["username"]) | (User.email == data["email"])
    ).first()

    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 409

    # Create new user
    new_user = User(username=data["username"], email=data["email"])
    new_user.set_password(data["password"])

    try:
        db.session.add(new_user)
        db.session.commit()

        # Generate access token
        access_token = create_access_token(identity=new_user.id)

        return jsonify(
            {
                "message": "User registered successfully",
                "user": new_user.to_dict(),
                "access_token": access_token,
            }
        ), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User login endpoint
    """
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    # Find user by username
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        # Generate access token
        access_token = create_access_token(identity=user.id)

        return jsonify(
            {
                "message": "Login successful",
                "user": user.to_dict(),
                "access_token": access_token,
            }
        ), 200

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Get user profile endpoint
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    User logout endpoint
    """
    # With JWT, logout is typically handled client-side by removing the token
    return jsonify({"message": "Logout successful"}), 200
