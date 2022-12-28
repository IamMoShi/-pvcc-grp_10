from flask import Blueprint, render_template, redirect, session
from os import listdir

from ..database.get_db import get_db
from ..fonctions.main.enleve_crochets import enleve_crochets
from ..fonctions.potager.html_code_fonction import html_code_fonction
from ..fonctions.potager.affichage_parcelle import affichage_parcelle
from ..fonctions.potager.legende_fonction import legende_fonction
from ..fonctions.potager.string_to_lists import string_to_lists

user = Blueprint('user', __name__)


@user.route('/users')
def users():
    if not session.get("email"):
        return redirect("/signin")
    else:
        db = get_db()
        items = db.cursor()

        items.execute("SELECT u.id_user, u.nom, u.prenom, u.mail, u.img FROM utilisateur u")
        data = items.fetchall()
        final = []

        for i in data:
            statut = ""
            items.execute(
                "SELECT u.id_user FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.id_user LIKE ?",
                (i[0],))
            admin = items.fetchall()
            if len(admin) != 0:
                statut += "- administrateur.trice "
            items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (i[0],))
            if len(items.fetchall()) != 0:
                statut += "- jardinier "
            items.execute("SELECT id_jardin FROM jardin WHERE id_referent LIKE ?", (i[0],))
            if len(items.fetchall()) != 0:
                statut += "- référent.e "

            statut += " - "
            i += (statut,)
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
            i += (i[4],)
            items.execute("SELECT id_jardin FROM jardin WHERE id_referent LIKE ?", (i[0],))
            ref = items.fetchall()
            i += (enleve_crochets(ref),)

            final.append(i)
        return render_template("users.html", data=final)


@user.route('/users/<numero>')
def userss(numero):
    if not session.get("email"):
        return redirect("/signin")

    # # vérifie que l'utilisateur a bien accès à ce jardin (qu'il a pas triché)
    # listeJardins = []
    # for i in session.get("parcelles"):
    #     db = get_db()
    #     items = db.cursor()
    #     items.execute(
    #         "SELECT p.id_jardin FROM parcelle p JOIN utilisateur u ON p.id_user=u.id_user WHERE id_parcelle=?", (i,))
    #     listeJardins.append((items.fetchall())[0][0])

    # cestpasbon = True
    # for j in listeJardins:
    #     if int(numero) == int(j):
    #         cestpasbon = False

    # """Bon en fait non, pas de condition pour voir les jardiniers c'est complicado avec les histoires d'admins, référents, ..."""
    # # si l'utilisateur ne fait pas partie du jardin demandé en numéro
    # # if cestpasbon==True:
    # #     return render_template("error_page.html", msg="Vous n'avez pas accès à ce jardin")

    # # else:
    db = get_db()
    items = db.cursor()

    items.execute(
        "SELECT DISTINCT u.id_user, u.nom, u.prenom, u.mail, u.img FROM utilisateur u JOIN parcelle p ON p.id_user=u.id_user WHERE p.id_jardin=? UNION SELECT u.id_user, u.nom, u.prenom, u.mail, u.img FROM utilisateur u JOIN administre a ON a.id_user=u.id_user WHERE a.id_jardin=? UNION SELECT u.id_user, u.nom, u.prenom, u.mail, u.img FROM utilisateur u JOIN jardin j ON j.id_referent=u.id_user WHERE j.id_jardin=?",
        (numero, numero, numero,))
    data = items.fetchall()
    final = []

    for i in data:
        statut = ""
        items.execute(
            "SELECT u.id_user FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.id_user LIKE ? AND a.id_jardin=?",
            (i[0], numero,))
        admin = items.fetchall()
        if len(admin) != 0:
            statut += "- administrateur.trice "
        items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ? AND id_jardin=?", (i[0], numero,))
        if len(items.fetchall()) != 0:
            statut += "- jardinier"
        items.execute("SELECT id_jardin FROM jardin WHERE id_referent LIKE ? AND id_jardin=?", (i[0], numero,))
        if len(items.fetchall()) != 0:
            statut += "- référent.e"
        statut += " - "
        i += (statut,)
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
        i += (i[4],)
        items.execute("SELECT id_jardin FROM jardin WHERE id_referent LIKE ?", (i[0],))
        ref = items.fetchall()
        i += (enleve_crochets(ref),)

        final.append(i)

    return render_template("users.html", data=final, numero=numero)


@user.route('/mesparcelles')
def mesparcelles():
    database = get_db()
    items = database.cursor()
    resultat = []
    if len(session["parcelles"]) == 0:
        return render_template("error_page.html",
                               msg="Vous n'avez pas encore de parcelles, contactez un administrateur pour qu'il vous en attribue une!")

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
        l_polygone = string_to_lists(l_polygone)
        l_id = string_to_lists(l_id)

        longueur, largeur = round(longueur), round(largeur)

        l_polygone_txt, chemin_image = html_code_fonction(l_polygone, l_id, id_parcelle)

        chemin_image = affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                                          database.cursor())

        l_polynomes_txt = l_polygone_txt[::-1]
        l_legende = legende_fonction(database.cursor(), l_id)

        parametres.append([l_polynomes_txt, l_legende, chemin_image, id_parcelle, id_jardin])

    chemin = "potager_user/potager_user_affichage_global.html"
    return render_template(chemin, parametres=parametres)


# affichage individuel des parcelles (fonction d'ajout de plantes à mettre)
@user.route('/mesparcelles/<numero>')
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

    # vérifie que l'utilisateur a bien accès à cette parcelle (et qu'il a pas triché)
    cestpasbon = True
    for num in session.get("parcelles"):
        if num == numero:
            cestpasbon = False
    if cestpasbon:
        return render_template("error_page.html", msg="Vous n'avez pas accès à cette parcelle")

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
    l_polygone = string_to_lists(l_polygone)
    l_id = string_to_lists(l_id)

    longueur, largeur = round(longueur), round(largeur)

    l_polygone_txt, chemin_image = html_code_fonction(l_polygone, l_id, id_parcelle)

    chemin_image = affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                                      database.cursor())

    chemin = "potager_user/potager_user_affichage_individuel.html"
    print(chemin_image)

    return render_template(chemin, l_polynomes_txt=l_polygone_txt[::-1], chemin_image=chemin_image,
                           l_legende=legende_fonction(database.cursor(), l_id), numero=numero,
                           id_jardin=id_jardin)


@user.route('/user/vos_informations')
def vos_informations():
    if not session.get("email"):
        return redirect("/signin")
    # try:
    #     numero = int(numero)
    # except:
    #     return 'error ce numero n\'est pas correct'

    db = get_db()
    # items = db.cursor()
    # items.execute('SELECT count(*) FROM parcelle WHERE id_user = ?', (session.get("id_user"),))
    # if not items.fetchall()[0]:
    #     return render_template('error_page.html', msg='Vous n\'avez pas accès à ces informations')

    items = db.cursor()
    items.execute('SELECT nom, prenom, mail, img FROM utilisateur WHERE id_user = ?', (session.get("id_user"),))
    resultat = items.fetchall()[0]

    if items == []:
        return 'La page demandé n\'existe pas'
    msg = None
    if len(session['parcelles']) == 0:
        msg = "Vous n'avez pas encore de parcelles, contactez un administrateur pour qu'il vous en attribue une!"

    donnees = {
        'lastname': resultat[0],
        'firstname': resultat[1],
        'email': resultat[2],
        'img': resultat[3]
    }

    items = db.cursor()
    items.execute('SELECT * FROM parcelle WHERE id_user = ?', (session.get("id_user"),))
    resultat = items.fetchall()
    parcelles = {}
    liste_parcelles = []

    for i in resultat:
        liste_parcelles.append(i[0])
        parcelles.update({
            i[0]: i[1::]
        })
    donnees.update({'parcelles': liste_parcelles})

    if session['admin'] == 'oui':
        jardins = []
        for i in session.get('num_jardin_a'):
            items = db.cursor()
            items.execute(
                'SELECT j.id_jardin, j.code_postal, j.ville, j.numero_rue, j.nom_rue, j.id_referent, u.prenom, u.nom FROM jardin j JOIN utilisateur u ON u.id_user=j.id_referent WHERE id_jardin = ?',
                (i,))
            jardins.append(items.fetchall()[0])
        return render_template('potager_user/user_page.html', donnees=donnees, parcelles=parcelles, jardins=jardins)

    return render_template('potager_user/user_page.html', donnees=donnees, parcelles=parcelles, msg=msg)


@user.route('/changePhoto')
def changePhoto():
    if not session["id_user"]:
        return redirect('/')

    listeImg = listdir("static/images/photos_profil")

    return render_template('changePhoto.html', listeImg=listeImg)


@user.route('/changePhoto/<chemin>')
def changePhotoo(chemin):
    db = get_db()
    items = db.cursor()
    items.execute("UPDATE utilisateur SET img=? WHERE id_user=?",
                  ("/static/images/photos_profil/" + chemin, session.get('id_user'),))
    db.commit()

    return redirect('/user/vos_informations')


@user.route('/monpotager/<numero>/edit')
def edit_potager(numero):
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    return render_template('potager_user/edit_potager.html')
