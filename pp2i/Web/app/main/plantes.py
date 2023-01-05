from flask import Blueprint, render_template

from ..database.get_db import get_db
from ..fonctions.plante.amis_ennemis import amis_ennemis

plante = Blueprint('plante', __name__)


@plante.route('/id_plante/<numero>')
def id_plante(numero):

    return str(amis_ennemis(numero, get_db()))
