from flask import render_template, Blueprints, session, redirect
from ..database.get_db import get_db
from ..fonctions.main.enleve_crochets import enleve_crochets
from ..fonctions.potager import transformation_polygone_v2 as tp
from ..fonctions.potager import image as image_py

user = Blueprints('user', __name__)


@user.route('/users')
def users():
    if not session.get("email"):
        return redirect("/signin")
    else:
        db = get_db()
        items = db.cursor()

        items.execute("SELECT u.id_user, u.nom, u.prenom, u.mail FROM utilisateur u")
        data = items.fetchall()
        final = []

        for i in data:
            items.execute(
                "SELECT u.id_user FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.id_user LIKE ?",
                (i[0],))
            admin = items.fetchall()
            if len(admin) != 0:
                i += ("admin",)
            else:
                i += ("pas admin",)
            # recupere les jardins de chacun
            items.execute(
                "SELECT a.id_jardin FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.id_user LIKE ?",
                (i[0],))
            num_jardin_a = items.fetchall()
            i += (enleve_crochets(num_jardin_a),)
            # recupere les parcelles de chacun
            items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (i[0],))
            parc = items.fetchall()
            i += (enleve_crochets(parc),)
            final.append(i)

        return render_template("users.html", data=final)


@user.route('/mesparcelles')
def mesparcelles():
    database = get_db()
    items = database.cursor()
    resultat = []
    if len(session["parcelles"]) == 0:
        return render_template("error_page.html", msg="Vous n'avez pas encore de parcelles")

    for i in range(len(session["parcelles"])):
        items.execute(
            'SELECT id_parcelle, id_jardin, longueur_parcelle, largeur_parcelle, polygone FROM parcelle WHERE id_parcelle = ?',
            (session["parcelles"][i],))
        resultat.append(items.fetchall())

    for i in range(len(resultat)):
        tmp = resultat[i][0]
        resultat[i] = tmp

    parametres = []
    for i in range(len(resultat)):
        id_parcelle, id_jardin, longueur, largeur, polygone = resultat[i]
        l_polygone, l_id = polygone.split('//')
        l_polygone = tp.string_to_lists(l_polygone)
        l_id = tp.string_to_lists(l_id)

        longueur, largeur = round(longueur), round(largeur)

        l_polygone_txt, chemin_image = image_py.html_code_fonction(l_polygone, l_id, id_parcelle)

        chemin_image = image_py.affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                                                   database.cursor())

        l_polynomes_txt = l_polygone_txt[::-1]
        l_legende = image_py.legende_fonction(database.cursor(), l_id)

        parametres.append([l_polynomes_txt, l_legende, chemin_image, id_parcelle])

    chemin = "potager_user/potager_user_affichage_global.html"
    return render_template(chemin, parametres=parametres)


# affichage individuel des parcelles (fonction d'ajout de plantes à mettre)


@user.route('/monpotager/<numero>')
def mon_potager(numero):
    """
    Verifier que la fonction tourne après la modification des paramètres sessions par ajout de id_user
    :param numero:
    :return:
    """
    if not session.get("email"):
        return redirect("/signin")
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    database = get_db()
    items = database.cursor()
    items.execute(
        'SELECT id_parcelle, id_jardin, longueur_parcelle, largeur_parcelle, polygone FROM parcelle WHERE id_parcelle = ?',
        (numero,))
    resultat = items.fetchall()
    if len(resultat) == 0:
        return 'la parcelle n\' a pas été trouvée'

    resultat = resultat[0]

    id_parcelle, id_jardin, longueur, largeur, polygone = resultat
    l_polygone, l_id = polygone.split('//')
    l_polygone = tp.string_to_lists(l_polygone)
    l_id = tp.string_to_lists(l_id)

    longueur, largeur = round(longueur), round(largeur)

    l_polygone_txt, chemin_image = image_py.html_code_fonction(l_polygone, l_id, id_parcelle)

    chemin_image = image_py.affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                                               database.cursor())

    chemin = "potager_user/potager_user_affichage_individuel.html"
    print(chemin_image)

    return render_template(chemin, l_polynomes_txt=l_polygone_txt[::-1], chemin_image=chemin_image,
                           l_legende=image_py.legende_fonction(database.cursor(), l_id), numeor=numero)


@user.route('/user/vos_informations/<numero>')
def vos_informations(numero):
    if not session.get("email"):
        return redirect("/signin")
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    db = get_db()
    items = db.cursor()
    items.execute('SELECT count(*) FROM parcelle WHERE id_user = ?', (session.get("id_user")))
    if not items.fetchall()[0]:
        return render_template('error_page.html', msg='Vous n\'avez pas accès à ces informations')

    items = db.cursor()
    items.execute('SELECT nom, prenom, mail FROM utilisateur WHERE id_user = ?', (numero,))
    resultat = items.fetchall()[0]

    if items == []:
        return 'La page demandé n\'existe pas'

    donnees = {
        'lastname': resultat[0],
        'firstname': resultat[1],
        'email': resultat[2]
    }

    items = db.cursor()
    items.execute('SELECT * FROM parcelle WHERE id_user = ?', (numero,))
    resultat = items.fetchall()
    parcelles = {}
    liste_parcelles = []

    for i in resultat:
        liste_parcelles.append(i[0])
        parcelles.update({
            i[0]: i[1::]
        })
    donnees.update({'parcelles': liste_parcelles})

    return render_template('potager_user/user_page.html', donnees=donnees, parcelles=parcelles)


@user.route('/monpotager/<numero>/edit')
def edit_potager(numero):
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    return render_template('potager_user/edit_potager.html')
