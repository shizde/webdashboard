# This __init__.py ensures that the routes directory is treated as a Python package
# It can be used to import and expose route blueprints or do any package-level configurations

from flask import Blueprint

# Create base blueprint that can be used for common route configurations
base_blueprint = Blueprint("base", __name__)


# You can add any package-level middleware or error handlers here
@base_blueprint.errorhandler(404)
def not_found(error):
    """
    Custom 404 error handler
    """
    return {
        "error": "Not found",
        "message": "The requested resource could not be found",
    }, 404


@base_blueprint.errorhandler(500)
def server_error(error):
    """
    Custom 500 error handler
    """
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred on the server",
    }, 500


# Import specific route blueprints to ensure they are registered
from .auth_routes import auth_bp
from .expense_routes import expense_bp
from .event_routes import event_bp

# List of all blueprints for easy registration
route_blueprints = [auth_bp, expense_bp, event_bp]
