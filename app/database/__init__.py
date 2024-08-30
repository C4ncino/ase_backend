"""
Database class and Models
"""

from .models.users import User
from .database_class import DatabaseInterface

database = DatabaseInterface()

__all__ = ['User', 'DatabaseInterface', 'database']
