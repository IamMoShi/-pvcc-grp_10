from flask import Blueprint, render_template

from ..database.get_db import get_db
from ..fonctions.potager.amis_ennemis import amis_ennemies

plante = Blueprint('plante', __name__)


@plante.route('/id_plante/<numero>')
def id_plante(numero):

    try:
        int(numero)
    except:
        return render_template("error_page.html", msg="Une erreur concernant le numéro de la plante est survenue")

    database = get_db()

    items = database.cursor()
    items.execute('select * from plante where id_plante = ?', (numero,))

    resultat = items.fetchall()

    if not resultat:
        return render_template("error_page.html", msg="Aucune plante ne possède cet id")

    id_plante, taille, nom, color = resultat[0]

    items = database.cursor()
    items.execute('Select * from compagnons where plante1 = ? or plante2 = ?', (id_plante, id_plante,))

    amis = items.fetchall()

    if not amis:
        return render_template("error_page.html", msg="Une erreur est survenue")

    amis = amis_ennemies(id_plante, amis)
