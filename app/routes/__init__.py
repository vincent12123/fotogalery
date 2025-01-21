from flask import Flask
from .test import test_bp
from .auth import auth_bp
from .main import main_bp
from .album import album_bp
from .foto import foto_bp


def register_blueprints(app):
    app.register_blueprint(test_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(album_bp)
    app.register_blueprint(foto_bp)
