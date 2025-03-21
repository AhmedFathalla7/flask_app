from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)

    from app.auth.routes import auth
    from app.main.routes import main

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(main, url_prefix='/')

    return app







