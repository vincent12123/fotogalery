import os
from flask import Config, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text

# Inisialisasi ekstensi
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Konfigurasi aplikasi
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gallery.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi ekstensi
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    

   # Daftarkan Blueprint
    from .routes import register_blueprints
    register_blueprints(app)
    
    with app.app_context():
        from app import models

    return app