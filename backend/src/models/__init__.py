# This __init__.py ensures that the models directory is treated as a Python package
# It can be used to import and expose models at the package level

from .user import User
from .expense import Expense
from .event import Event

# You can add any package-level configurations or imports here
__all__ = ["User", "Expense", "Event"]
