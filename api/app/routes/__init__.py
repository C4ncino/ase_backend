"""
Application routes
"""

from .users import users_bp
from .words import words_bp
from .models import models_bp
from .base import base_bp

__all__ = ['base_bp', 'words_bp', 'users_bp', 'models_bp']
