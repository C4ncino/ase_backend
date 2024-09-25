"""
Main App
"""
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import AppConfig
from .utils import celery_init_app
from app.routes import base_bp, users_bp, words_bp, models_bp, training_bp
# -----------------------------------------------------------------------------

app = Flask(__name__)

app.config.from_object(AppConfig)

celery_app = celery_init_app(app)

CORS(app)

JWTManager(app)

# -----------------------------------------------------------------------------

app.register_blueprint(base_bp)
app.register_blueprint(users_bp)
app.register_blueprint(words_bp)
app.register_blueprint(models_bp)
app.register_blueprint(training_bp)

# -----------------------------------------------------------------------------

__all__ = ['app', 'celery_app']
