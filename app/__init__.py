"""
Main App
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import AppConfig
from app.routes import users_bp, words_bp, models_bp
# -----------------------------------------------------------------------------

app = Flask(__name__)

app.config.from_object(AppConfig)

CORS(app)

JWTManager(app)

# -----------------------------------------------------------------------------

app.register_blueprint(users_bp)
app.register_blueprint(words_bp)
app.register_blueprint(models_bp)

# -----------------------------------------------------------------------------

__all__ = ['app', 'database']
