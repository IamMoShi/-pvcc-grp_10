from flask import Blueprint, render_template

plante = Blueprint('plante', __name__)


@plante.route('/id_plante/<numero>')
def id_plante(numero):
    return numero
