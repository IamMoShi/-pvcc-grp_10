from flask import Blueprint, render_template

from ..database.get_db import get_db
from ..fonctions.plante.amis_ennemis import amis_ennemis

plante = Blueprint('plante', __name__)


@plante.route('/id_plante/<numero>')
def id_plante(numero):
    l_infos_amis, l_info_ennemis, dico_des_erreurs, erreur = amis_ennemis(numero, get_db())
    if erreur == 1 or erreur == 2:
        return render_template("error_page", msg="")

    resultat = get_db().cursor().execute("Select * from plante where id_plante = ?", (numero,)).fetchall()[0]
    id_plante, taille, nom_plante, couleur = resultat

    return render_template("plante/plante.html", l_infos_amis=l_infos_amis, l_info_ennemis=l_info_ennemis, nom_plante=nom_plante)
