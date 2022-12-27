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
    from .main.authentication import authentication
    from .main.user import user
    from .main.admin import admin
    from .main.plantes import plante
    # ====================
    """
    Utilisation des blueprints
    """
    # ====================
    app.register_blueprint(main)
    app.register_blueprint(authentication)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(plante)

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app
