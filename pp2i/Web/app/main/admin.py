from flask import render_template, Blueprint, session, request
from ..database.get_db import get_db
from ..fonctions.potager import image as image_py

admin = Blueprint('admin', __name__)


@admin.route('/admin/nouvelle_parcelle')
def nouvelle_parcelle():
    if session['admin'] == 'oui':
        return render_template('admin/nouvelle_parcelle.html')
    else:
        return render_template('error_page.html', msg="Vous n'avez pas les droits d'administrateur")


@admin.route('/send-creer-parcelle', methods=['POST', 'GET'])
def definir_parcelle_post():
    """
    Ajouter la vérification du compte administrateur et faire agir la page en conséquence
    :return:
    """
    if request.method == "POST":
        try:
            largeur = int(request.form['largeur'])
            longueur = int(request.form['longueur'])
            id_jardin = request.form['id_jardin']
            parcelle = image_py.NouvelleParcelle(longueur, largeur)
        except:
            return 'ERROR'

        db = get_db()
        items = db.cursor()
        items.execute(
            'INSERT INTO parcelle (id_jardin, longueur_parcelle, largeur_parcelle, polygone) VALUES (?,?,?,?)',
            (id_jardin, longueur, largeur, str(parcelle.l_polygones) + "//[0]",)
        )
        db.commit()

        db = get_db()
        items = db.cursor()
        items.execute('SELECT max(id_parcelle) FROM parcelle')
        id_image = items.fetchall()[0][0]
        return render_template('success_page.html', msg="La parcelle a bien été ajoutée !")

    return render_template('error_page.html', msg="Une erreur est survenue lors de l'ajout")


@admin.route('/admin/attribution_parcelles')
def attribution_parcelles():
    """
    AJOUTER Id_user rapidement !!
    :return:
    """
    if not session.get("email"):
        return redirect("/signin")
    if not session["admin"]:
        return render_template('error_page.html', msg='Vous n\'êtes administrateur d\'aucun jardin')

    db = get_db()
    items = db.cursor()
    items.execute('SELECT id_jardin, numero_rue, nom_rue, ? FROM jardin WHERE id_referent LIKE ?',
                  (session["num_jardin_a"][0], session["id_user"]))
    resultat = items.fetchall()

    return render_template('admin/attribution_parcelle.html', resultat=resultat)

@admin.route('/test')
def test():
    resultat = [[1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50]]],
                [1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50], [22, 1, 120, 50]]],
                [1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50]]]]
    return render_template('admin/attribution_parcelle.html', resultat=resultat)
