from flask import Flask
from .test import test_bp
from .auth import auth_bp


def register_blueprints(app):
    app.register_blueprint(test_bp)
    app.register_blueprint(auth_bp)
    
