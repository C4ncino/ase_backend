"""
Database class and Models
"""

from .models.example import Example
from .database_class import DatabaseInterface

database = DatabaseInterface()

__all__ = ['Example', 'DatabaseInterface', 'database']
