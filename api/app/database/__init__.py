"""
Database class and Models
"""

from .models.words import Word
from .models.users import User
from .models.data_words import Data
from .database_class import DatabaseInterface

database = DatabaseInterface()

__all__ = ['DatabaseInterface', 'database', 'User', 'Word', 'Data']
