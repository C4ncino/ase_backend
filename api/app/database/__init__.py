"""
Database class and Models
"""

from .models.word import Word
from .models.users import User
from .models.models import Model
from .database_class import DatabaseInterface

database = DatabaseInterface()

__all__ = ['DatabaseInterface', 'database', 'User', 'Word', 'Model']
