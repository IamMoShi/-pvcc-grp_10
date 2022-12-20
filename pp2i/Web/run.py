from flask import g
from app import create_app

if __name__ == '__main__':
    create_app().run(debug=True)
    app = create_app()

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
