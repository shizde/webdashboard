import logging
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def handle_validation_error(error):
    """
    Handle validation errors with consistent error response

    Args:
        error (Exception): Validation error to handle

    Returns:
        tuple: Flask response with error details
    """
    logger.warning(f"Validation Error: {str(error)}")
    return jsonify(
        {"status": "error", "type": "validation", "message": str(error)}
    ), 400


def handle_database_error(error):
    """
    Handle database-related errors with consistent error response

    Args:
        error (SQLAlchemyError): Database error to handle

    Returns:
        tuple: Flask response with error details
    """
    logger.error(f"Database Error: {str(error)}")
    return jsonify(
        {
            "status": "error",
            "type": "database",
            "message": "An unexpected database error occurred",
        }
    ), 500


def handle_authentication_error(error):
    """
    Handle authentication-related errors

    Args:
        error (Exception): Authentication error to handle

    Returns:
        tuple: Flask response with error details
    """
    logger.warning(f"Authentication Error: {str(error)}")
    return jsonify(
        {"status": "error", "type": "authentication", "message": str(error)}
    ), 401


def global_error_handler(error):
    """
    Global error handler for unexpected errors

    Args:
        error (Exception): Unexpected error to handle

    Returns:
        tuple: Flask response with error details
    """
    logger.critical(f"Unhandled Error: {str(error)}", exc_info=True)
    return jsonify(
        {
            "status": "error",
            "type": "unexpected",
            "message": "An unexpected error occurred",
        }
    ), 500


class CustomErrorHandler:
    """
    Custom error handling class with advanced error management
    """

    @staticmethod
    def log_error(error, level="error"):
        """
        Log errors with different severity levels

        Args:
            error (Exception): Error to log
            level (str): Logging level
        """
        log_methods = {
            "debug": logger.debug,
            "info": logger.info,
            "warning": logger.warning,
            "error": logger.error,
            "critical": logger.critical,
        }

        log_method = log_methods.get(level, logger.error)
        log_method(f"Error: {str(error)}", exc_info=True)

    @staticmethod
    def create_error_response(message, status_code=400, error_type="generic"):
        """
        Create a standardized error response

        Args:
            message (str): Error message
            status_code (int): HTTP status code
            error_type (str): Type of error

        Returns:
            tuple: Flask response with error details
        """
        return jsonify(
            {"status": "error", "type": error_type, "message": message}
        ), status_code
