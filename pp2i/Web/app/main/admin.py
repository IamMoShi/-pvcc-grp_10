from flask import Blueprint, render_template, session, request, redirect

from ..database.get_db import get_db
from ..fonctions.potager.NouvelleParcelle import NouvelleParcelle
from ..fonctions.main.enleve_crochets import enleve_crochets

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
            parcelle = NouvelleParcelle(longueur, largeur)
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
    items.execute(
        'SELECT j.id_jardin, j.numero_rue, j.nom_rue, j.code_postal, j.ville, j.id_referent, u.prenom, u.nom FROM jardin j JOIN administre a ON a.id_jardin=j.id_jardin JOIN utilisateur u ON u.id_user=j.id_referent WHERE a.id_user=?',
        (session["id_user"],))
    resultat = items.fetchall()

    for i in range(len(resultat)):
        items.execute(
            "SELECT p.id_parcelle, p.longueur_parcelle, p.largeur_parcelle, p.id_user, u.prenom, u.nom FROM parcelle p JOIN utilisateur u ON u.id_user=p.id_user WHERE id_jardin=?",
            (resultat[i][0],))
        resultat[i] += ((items.fetchall()),)

    liste_jardiniers = []
    items.execute('SELECT id_user, prenom, nom FROM utilisateur')
    liste_jardiniers.append(items.fetchall())
    return render_template('admin/attribution_parcelle.html', resultat=resultat, liste_jardiniers=liste_jardiniers)


@admin.route('/admin/supp_parcelle/<num_parcelle>')
def supp_parcelle(num_parcelle):
    if not session.get("email"):
        return redirect("/signin")
    if not session["admin"]:
        return render_template('error_page.html', msg='Vous n\'êtes administrateur d\'aucun jardin')
    db = get_db()
    items = db.cursor()
    items.execute('DELETE FROM parcelle WHERE id_parcelle=?', (num_parcelle,))
    db.commit()

    # for i in range(len(session['parcelles'])):
    #     if int(session['parcelles'][i]) == int(num_parcelle):
    #         del session['parcelles'][i]
    #         break

    items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (session['id_user'],))
    parc = items.fetchall()
    session["parcelles"] = enleve_crochets(parc)

    return redirect('/admin/attribution_parcelles')


@admin.route('/admin/ajouter_parcelle', methods=['POST', 'GET'])
def ajouter_parcelle():
    if not session.get("email"):
        return redirect("/signin")
    if not session["admin"]:
        return render_template('error_page.html', msg='Vous n\'êtes administrateur d\'aucun jardin')
    if request.method == 'POST':
        db = get_db()
        items = db.cursor()
        # items.execute('SELECT max(id_parcelle) FROM parcelle')
        # new_id = int(items.fetchall()[0][0]) + 1
        jardinier = request.form.get('jardinier')[0]

        largeur = int(request.form.get('largeur'))
        longueur = int(request.form.get('longueur'))
        id_jardin = request.form.get('num_jardin')
        parcelle = NouvelleParcelle(longueur, largeur)

        items.execute(
            'INSERT INTO parcelle (id_jardin, id_user, longueur_parcelle, largeur_parcelle, polygone) VALUES (?,?,?,?,?)',
            (id_jardin, jardinier, longueur, largeur, str(parcelle.l_polygones) + "//[0]",)
            )
        db.commit()
        items.execute(
            'SELECT id_parcelle from parcelle where id_jardin=? and id_user=? and longueur_parcelle=? and largeur_parcelle=?',
            (id_jardin, jardinier, longueur, largeur,)
            )
        new_id = (items.fetchall())

        if int(jardinier) == int(session.get('id_user')):
            items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (session['id_user'],))
            parc = items.fetchall()
            session["parcelles"] = enleve_crochets(parc)

        return redirect('/admin/attribution_parcelles')
