"""
Main App
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import AppConfig
from app.routes import example_bp

# -----------------------------------------------------------------------------

app = Flask(__name__)

app.config.from_object(AppConfig)

CORS(app)

JWTManager(app)

# -----------------------------------------------------------------------------

app.register_blueprint(example_bp)

# -----------------------------------------------------------------------------

__all__ = ['app', 'database']
