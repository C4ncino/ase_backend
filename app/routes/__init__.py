"""
Application routes
"""

from .example_routes import example_bp
from .users import users_bp
from .words import words_bp

__all__ = ['words_bp', 'users_bp']
