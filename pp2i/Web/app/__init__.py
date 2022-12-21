from flask import Flask
from flask_session import Session


def create_app():
    app = Flask(__name__)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    from .main.main import main
    # from .main.auth import auth
    # from .main.admin import admin
    # from .main.user import user
    # from .main.plante import plante

    app.register_blueprint(main)
    #app.register_blueprint(auth)
    return app

