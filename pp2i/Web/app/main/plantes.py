from flask import Blueprint

plante = Blueprint('plante', __name__)


@plante.route('/id_plante/<numero>')
def id_plante(numero):
    return numero
