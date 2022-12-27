from flask import Flask, g
from flask_session import Session


def create_app():
    app = Flask(__name__)

    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # ====================
    """
    Import des blueprints
    """
    # ====================
    from .main.main import main

    # ====================
    """
    Utilisation des blueprints
    """
    # ====================
    app.register_blueprint(main)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app
