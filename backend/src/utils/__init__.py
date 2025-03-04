# This __init__.py ensures that the utils directory is treated as a Python package
# It can be used to import and expose utility modules or do any package-level configurations

# Import specific utility modules
from .db_connection import create_db_connection
from .validators import validate_email, validate_password
from .error_handlers import handle_validation_error, handle_database_error

# List of all utilities for potential global access
__all__ = [
    "create_db_connection",
    "validate_email",
    "validate_password",
    "handle_validation_error",
    "handle_database_error",
]


# Optional package-level configuration or utility methods
class UtilityRegistry:
    """
    A simple utility registry to manage and access utility functions
    """

    _utilities = {}

    @classmethod
    def register(cls, name, utility):
        """
        Register a utility function with the registry
        """
        cls._utilities[name] = utility

    @classmethod
    def get(cls, name):
        """
        Retrieve a utility function from the registry
        """
        return cls._utilities.get(name)
