from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/status')
def index():
    return 'Up and Running'


@main.route('/')
def accueil():
    return render_template("accueil.html")
