import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .views import views

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    controller_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(controller_dir, "..", "templates")

    app = Flask(__name__, template_folder=template_dir)
    app.config['SECRET_KEY'] = 'abcd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    
    #from auth import auth

    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    # from .models import User, Note'
    
    # with app.app_context():
    #     db.create_all()

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')