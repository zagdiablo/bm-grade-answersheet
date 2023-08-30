from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager  # TODO implement basic login
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash
from . import config

import os


app = Flask(__name__)
db = SQLAlchemy(app)


#
#
#
#
# create flask aplication instance
#
def create_app(config_name="DevelopmentConfig"):
    """
    create an app instance of flask to run a web application

    config_name = the name of a config object inside config.py
    """

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config.from_object(config.DevelopmentConfig)

    # Blueprints
    from .user_auth import user_auth
    from .user_views import user_views
    from .admin_auth import admin_auth
    from .admin_views import admin_views

    app.register_blueprint(user_auth, url_prefix="/")
    app.register_blueprint(user_views, url_prefix="/")
    app.register_blueprint(admin_auth, url_prefix="/")
    app.register_blueprint(admin_views, url_prefix="/")

    # Error handler
    from .error_handler import unauthorized_401

    app.register_error_handler(401, unauthorized_401)

    # user login configuration
    login_manager = LoginManager(app)

    # user loader to load user from database models for login manager
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # any other needed configuration or module
    # ex: csrf_protect(app), db_init(app)
    csrf = CSRFProtect(app)

    # database configuration
    db.init_app(app)
    if not check_database():
        db.create_all()

    # admin account generation
    generate_admin_account()

    return app


#
# 
def check_database():
    """
    check if database is exist

    return True/False
    """

    if os.path.isfile("database.db"):
        return True
    return False


#
#
def generate_admin_account():
    """
    generate admin account if no user with admin role in the database
    """

    from .models import User

    accounts = User.query.all()
    for account in accounts:
        if account.role == 'admin':
            print('[-] Admin account already exist, please login using that account.')
            return
    
    new_admin = User(
        username = 'admin',
        password = generate_password_hash('password', "pbkdf2:sha256"),
        role = 'admin'
    )
    db.session.add(new_admin)
    db.session.commit()

    print('[+] Admin account generation success.')