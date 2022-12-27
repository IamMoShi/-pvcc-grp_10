from flask import g, Flask
from flask_session import Session

from app import *

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
