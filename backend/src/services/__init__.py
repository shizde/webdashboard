# This __init__.py ensures that the services directory is treated as a Python package
# It can be used to import and expose service modules or do any package-level configurations

# Import specific service modules
from .expense_service import ExpenseService
from .event_service import EventService

# List of all services for potential global access
__all__ = ["ExpenseService", "EventService"]


# You can add any package-level service configurations or utility methods here
class ServiceRegistry:
    """
    A simple service registry to manage and access services
    """

    _services = {}

    @classmethod
    def register(cls, name, service):
        """
        Register a service with the registry
        """
        cls._services[name] = service

    @classmethod
    def get(cls, name):
        """
        Retrieve a service from the registry
        """
        return cls._services.get(name)
