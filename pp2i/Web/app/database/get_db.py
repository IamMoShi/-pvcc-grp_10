from flask import g
import sqlite3


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('app/database/database.db')
    return g.db
