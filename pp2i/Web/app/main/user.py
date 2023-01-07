from flask import Blueprint, render_template, redirect, session, request
from os import listdir

from ..database.get_db import get_db
from ..fonctions.main.enleve_crochets import enleve_crochets
from ..fonctions.potager.html_code_fonction import html_code_fonction
from ..fonctions.potager.affichage_parcelle import affichage_parcelle
from ..fonctions.potager.legende_fonction import legende_fonction
from ..fonctions.potager.string_to_lists import string_to_lists
from ..fonctions.potager import class_terrain
from ..fonctions.potager.PotagerImage import PotagerImage
from ..fonctions.plante.amis_ennemis import amis_ennemis
import re

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
        """SELECT DISTINCT u.id_user, u.nom, u.prenom, u.mail, u.img 
            FROM utilisateur u JOIN parcelle p ON p.id_user=u.id_user WHERE p.id_jardin=? 
            UNION SELECT u.id_user, u.nom, u.prenom, u.mail, u.img 
            FROM utilisateur u JOIN administre a ON a.id_user=u.id_user WHERE a.id_jardin=? 
            UNION SELECT u.id_user, u.nom, u.prenom, u.mail, u.img 
            FROM utilisateur u JOIN jardin j ON j.id_referent=u.id_user WHERE j.id_jardin=?""",
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
    # ----------------------------------------------------------------------------------------------------------#
    """
    Le but de cette fonction est d'afficher toutes les parcelles possédées par un utilisateur logger
    S'il n'est pas logger, alors le renvoyer vers la page de connection
    """
    # ----------------------------------------------------------------------------------------------------------#
    # ----------------On vérifie que la personne est bien connectée avec une session ---------------------------#

    if len(session["parcelles"]) == 0:
        return render_template("error_page.html",
                               msg="Vous n'avez pas encore de parcelles, contactez un administrateur pour qu'il vous en attribue une!")

    # ----------------------------------------------------------------------------------------------------------#
    # ----- Import de la base de donnée pour récupérer les informations sur les parcelles de la personne -------#

    database = get_db()
    items = database.cursor()
    resultat = []

    # ----------------------------------------------------------------------------------------------------------#
    # ------------------On fait une boucle sur toutes les parcelles de la personne -----------------------------#

    for i in range(len(session["parcelles"])):
        items.execute(
            'SELECT id_parcelle, id_jardin, longueur_parcelle, largeur_parcelle, polygone FROM parcelle WHERE id_parcelle = ?',
            (session["parcelles"][i],))
        resultat.append(items.fetchall())

    # ----------------------------------------------------------------------------------------------------------#
    # -------------- On ne récupère que la partie contenant les informations dans résultat ---------------------#

    for i in range(len(resultat)):
        tmp = resultat[i][0]
        resultat[i] = tmp

    # ----------------------------------------------------------------------------------------------------------#
    """
    On va maintenant passer à l'affichage des parcelles de l'utilisateur
    """
    # ----------------------------------------------------------------------------------------------------------#

    # -------------------------------------------- #
    # --- Paramètres nécessaire à la page html ----#

    parametres = []

    # -------------------------------------------- #

    for i in range(len(resultat)):  # On va faire le travail sur chaque parcelle

        # -------------------------------------------- #
        # --- Récupération des infos de la parcelle ---#

        id_parcelle, id_jardin, longueur, largeur, polygone = resultat[i]

        # -------------------------------------------- #
        # ---- récupération de l_polygone et l_id ---- #

        l_polygone, l_id = polygone.split('//')

        # -------------------------------------------- #
        # --------- transformation vers list --------- #

        l_polygone = string_to_lists(l_polygone)
        l_id = string_to_lists(l_id)

        # -------------------------------------------- #
        # ----------- Création de l'image ------------ #

        longueur, largeur = round(longueur), round(largeur)
        affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id, database.cursor())

        # -------------------------------------------- #
        # --------- transformation pour html --------- #

        l_polygone_txt, chemin_image = html_code_fonction(l_polygone, l_id, id_parcelle)

        # -------------------------------------------- #
        # ------- Problématique d'empilement --------- #

        l_polynomes_txt = l_polygone_txt[::-1]

        # -------------------------------------------- #
        # ------- Récupération de la légende --------- #

        l_legend = legende_fonction(database.cursor(), l_id)
        for i in range(len(l_legend)):
            items.execute("SELECT nom FROM plante WHERE id_plante=?", (l_legend[i][1],))
            l_legend[i] += (items.fetchone(),)

        # -------------------------------------------- #
        # ------------ Chemin de l'image ------------- #

        chemin_image = str(id_parcelle) + ".png"

        # -------------------------------------------- #
        # ---Récupération des données de paramètres--- #

        parametres.append([l_polynomes_txt, l_legend, chemin_image, id_parcelle, id_jardin])

    # -------------------------------------------- #
    # ------------ Chemin du template ------------ #

    chemin = "potager_user/potager_user_affichage_global.html"

    # -------------------------------------------- #

    return render_template(chemin, parametres=parametres)


# affichage individuel des parcelles (fonction d'ajout de plantes à mettre)
@user.route('/mesparcelles/<numero>')
def mon_potager(numero):
    """
    Verifier que la fonction tourne après la modification des paramètres sessions par ajout d'id_user
    :param numero:
    :return:
    """

    # ----------------------------------------------------- #
    # ----------- vérification de la connection------------ #

    if not session.get("email"):
        return redirect("/signin")
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    # ------------------------------------------------------------------------------------- #
    # --vérifie que l'utilisateur a bien accès à cette parcelle (et qu'il n'a pas triché)-- #

    cestpasbon = True
    for num in session.get("parcelles"):

        if num == numero:
            cestpasbon = False

    if cestpasbon:
        return render_template("error_page.html", msg="Vous n'avez pas accès à cette parcelle")

    # ----------------------------------------------------- #
    # --------- récupération de la base de données--------- #

    database = get_db()

    # ----------------------------------------------------- #
    # ---- récupération des informations de la parcelle---- #

    items = database.cursor()
    items.execute(
        'SELECT id_parcelle, id_jardin, longueur_parcelle, largeur_parcelle, polygone FROM parcelle WHERE id_parcelle = ?',
        (numero,))
    resultat = items.fetchall()

    # ----------------------------------------------------- #
    # ------------Cas où l'on a aucun résultat------------- #

    if len(resultat) == 0:
        return 'la parcelle n\' a pas été trouvée'

    # ----------------------------------------------------- #
    # ---------------Cas où l'on a un résultat------------- #

    resultat = resultat[0]

    # ----------------------------------------------------- #
    # -----récupération des informations de résultat------- #

    id_parcelle, id_jardin, longueur, largeur, polygone = resultat

    # ----------------------------------------------------- #
    # ---------récupération de l_polygone et l_id---------- #

    l_polygone, l_id = polygone.split('//')

    # ----------------------------------------------------- #
    # -----------Conversion de string vers liste----------- #

    l_polygone = string_to_lists(l_polygone)
    l_id = string_to_lists(l_id)

    # ----------------------------------------------------- #
    # --Conversion de float vers int (longueur et largeur)- #

    longueur, largeur = round(longueur), round(largeur)

    # ----------------------------------------------------- #
    # --------récupération de la liste pour le html-------- #

    l_polygone_txt, chemin_image = html_code_fonction(l_polygone, l_id, id_parcelle)

    # ----------------------------------------------------- #
    # --------Création de l'image de la parcelle----------- #

    affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                       database.cursor())

    # ----------------------------------------------------- #
    # ---Chemin d'ouverture de la page html et de l'image-- #

    chemin_image = str(id_parcelle) + ".png"
    chemin = "potager_user/potager_user_affichage_individuel.html"

    # ----------------------------------------------------- #
    # --Récupération de la liste des plantes pour l'ajout-- #

    items.execute('SELECT DISTINCT id_plante, nom FROM plante ORDER BY nom')
    plantes = items.fetchall()

    l_legend = legende_fonction(database.cursor(), l_id)
    for i in range(len(l_legend)):
        items.execute("SELECT nom FROM plante WHERE id_plante=?", (l_legend[i][1],))
        l_legend[i] += (items.fetchone(),)

    return render_template(chemin, l_polynomes_txt=l_polygone_txt[::-1], chemin_image=chemin_image,
                           l_legende=l_legend, numero=numero,
                           id_jardin=id_jardin, longueur=longueur, largeur=largeur, plantes=plantes)


@user.route('/mesparcelles/<numero>/ajouter_plante', methods=['POST', 'GET'])
def ajout_plante(numero):
    if not session.get("email"):
        return redirect("/signin")

    if request.method == 'POST':
        db = get_db()
        items = db.cursor()
        id_p = request.form['nom_plante']
        id_plante = int(re.findall('\d+', id_p)[0])
        x_plante = int(float(request.form['x_plante']))
        y_plante = int(float(request.form['y_plante']))

        items.execute("SELECT longueur_parcelle, largeur_parcelle FROM parcelle WHERE id_parcelle=?", (numero,))
        longueur, largeur = items.fetchall()[0]
        longueur = int(longueur)
        largeur = int(largeur)

        # creation du terrain vide
        terrain = class_terrain.Terrain((longueur, largeur))
        mon_terrain = terrain.creation_terrain()

        # infos de la plante à ajouter
        items.execute('SELECT * FROM plante WHERE id_plante=?', (id_plante,))
        id_plante, taille, nom, couleur = items.fetchall()[0]

        # ajouter les plantes déjà existantes dans le terrain
        items.execute("select id_plante,x_plante,y_plante from contient where id_parcelle like ?", (numero,))
        result = items.fetchall()
        for i in result:
            items.execute("select taille from plante where id_plante like ?", (i[0],))
            result2 = items.fetchall()
            mon_terrain, B, msg = terrain.ajout_plante(result2[0][0], (i[1], i[2]), i[0])

        # verification
        mon_nouveau_terrain, condition, msg = terrain.ajout_plante(taille, (x_plante, y_plante), id_plante)

        if not condition:  # si ça ne marche pas : on garde l'ancien terrain
            mon_terrain = mon_terrain
            msg = "Vous ne pouvez pas ajouter cette plante ici"
            return render_template("error_page.html", msg=msg)

        else:  # si c'est validé
            mon_terrain = mon_nouveau_terrain

        objet_image = PotagerImage(mon_terrain, numero, items)

        l_contour, l_polygone, alpha = objet_image.polygone()
        l_id = objet_image.l_id
        polygone = str(l_polygone) + "//" + str(l_id)

        # ajout de la plante dans la db si c'est validé :

        items.execute("UPDATE parcelle SET polygone=? WHERE id_parcelle=?", (polygone, numero,))
        items.execute("INSERT INTO contient VALUES (?,?,?,?)", (numero, id_plante, x_plante, y_plante,))
        db.commit()
        return redirect('/mesparcelles/' + str(numero))


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

    listeImg = listdir("app/static/images/photos_profil")

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


@user.route('/dico', methods=['GET', 'POST'])
def dico():
    num = request.args.get('num_plante')
    n = int(re.findall('\d+', num)[0])

    return redirect('/dico/' + str(n))


# page pour voir les affinités des plantes
@user.route('/dico/<num>')
def dicoo(num):
    # vérifier que la plante est dans la db (les id des plantes vont de 1 à 86)
    if (int(num) < 1 or int(num) > 86):
        return redirect('/mesparcelles')

    db = get_db()
    items = db.cursor()
    items.execute("SELECT id_plante, nom FROM plante ORDER BY nom")
    plantes = items.fetchall()

    items.execute("SELECT id_plante, nom FROM plante WHERE id_plante=? ORDER BY nom", (num,))
    plante_cherchee = items.fetchall()

    l_infos_amis, l_infos_ennemis, dico_des_erreurs, i = amis_ennemis(num, get_db())

    return render_template('dico.html', amis=l_infos_amis, ennemis=l_infos_ennemis, plantes=plantes,
                           plante_cherchee=plante_cherchee)
