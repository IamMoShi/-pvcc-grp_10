from flask import Blueprint, render_template, redirect, g
import sqlite3
from ..database.get_db import get_db

main = Blueprint('main', __name__)


