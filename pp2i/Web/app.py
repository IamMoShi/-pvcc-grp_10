from flask import Flask, render_template, request, redirect, g, session
from flask_session import Session
import back_python.login.register as register_py
import back_python.login.signin as signin_py
import back_python.login.hash as hash_py
import back_python.potager.image as image_py
import back_python.potager.transformation_polygone_v2 as tp
import sqlite3
import numpy as np

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE = 'database/database.db'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def enleveCrochets(liste):
    tmp = []
    if len(liste) != 0:
        for i in range(len(liste)):
            tmp.append(liste[i][0])
    return tmp


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/status')
def index():
    return 'Up and Running'


@app.route('/')
def accueil():
    return render_template("accueil.html")


@app.route('/signin')
def signin():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return render_template("login/login.html", b_signin=True, b_register=False)


@app.route('/register')
def signup():
    return render_template("login/login.html", b_signin=False, b_register=True)


@app.route('/login')
def login():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return render_template("login/login.html", b_signin=True, b_register=True)


@app.route('/logout')
def logout():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return redirect("/")


@app.route('/users')
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
            i += (enleveCrochets(num_jardin_a),)
            # recupere les parcelles de chacun
            items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (i[0],))
            parc = items.fetchall()
            i += (enleveCrochets(parc),)
            i+=("/static/images/icons/gardener.png",)
            final.append(i)

        return render_template("users.html", data=final)


@app.route('/users/<numero>')
def userss(numero):
    if not session.get("email"):
        return redirect("/signin")

    #vérifie que l'utilisateur a bien accès à ce jardin (qu'il a pas triché)
    listeJardins=[]
    for i in session.get("parcelles"):
        db = get_db()
        items = db.cursor()
        items.execute("SELECT p.id_jardin FROM parcelle p JOIN utilisateur u ON p.id_user=u.id_user WHERE id_parcelle=?", (i,))
        listeJardins.append((items.fetchall())[0][0])
    
    cestpasbon=True
    for j in listeJardins :
        if int(numero)==int(j):
            cestpasbon=False
    
    #si l'utilisateur ne fait pas partie du jardin demandé en numéro
    if cestpasbon==True:
        return render_template("error_page.html", msg="Vous n'avez pas accès à ce jardin")
    
    else:
        db = get_db()
        items = db.cursor()

        items.execute("SELECT u.id_user, u.nom, u.prenom, u.mail FROM utilisateur u JOIN parcelle p ON p.id_user=u.id_user WHERE id_jardin=?", (numero,))
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
            i += (enleveCrochets(num_jardin_a),)
            # recupere les parcelles de chacun
            items.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (i[0],))
            parc = items.fetchall()
            i += (enleveCrochets(parc),)
            i+=("/static/images/icons/gardener.png",)
            final.append(i)

        return render_template("users.html", data=final, numero=numero)

@app.route('/send-register-form', methods=['POST', 'GET'])
def register_post():
    if request.method == 'POST':

        last_name = request.form['lastname']
        first_name = request.form['firstname']
        email = request.form['email']
        password = request.form['password']
        confirmation = request.form['confirmation']

        validation = register_py.register(last_name, first_name, email, password, confirmation)

        if validation[0]:
            db = get_db()
            items = db.cursor()
            items.execute("SELECT count(*) FROM utilisateur WHERE mail LIKE ?", (email,))
            if len(items.fetchall()[0]) != 1:
                return redirect('/login')

            pwd_hash = hash_py.hash(password)
            items.execute('INSERT INTO utilisateur (nom, prenom, mail, mdp) VALUES (?,?,?,?)',
                          (last_name, first_name, email, pwd_hash))
            db.commit()
            return render_template('login/bienvenue.html', first_name=first_name, last_name=last_name)
    return 'ERROR'


# quand on se connecte à un compte
"""
le dictionnaire session comprend:
session["email"] :email
session["name"]: prénom nom de l'utilisateur
session["id_user"] = id de l'utilisateur
session["admin"] = "oui" si l'utilisateur est admin, sinon pas de valeur
session["num_jardin_a"] = [id_1, id_2, ...] renvoie les id des jardins dans lesquels on est admin
session["parcelles"]= [id_1, id_2, ...] renvoie les id des parcelles qu'on gère
"""


@app.route('/send-signin-form', methods=['POST', 'GET'])
def signin_post():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if signin_py.signin(email, password):
            pwd_hash = hash_py.hash(password)
            db = get_db()
            items = db.cursor()
            items.execute("SELECT count(*) FROM utilisateur WHERE mail LIKE ? and mdp = ? ", (email, pwd_hash,))
            if items.fetchall()[0][0] != 1:
                return render_template('login/erreur.html')

            else:
                session["email"] = request.form.get("email")
                dbb = get_db()
                itemss = dbb.cursor()
                itemss.execute("SELECT prenom, nom FROM utilisateur WHERE mail LIKE ? ", (email,))
                nom = itemss.fetchall()
                session["name"] = nom[0][0] + " " + nom[0][1]
                itemss.execute("SELECT id_user FROM utilisateur WHERE mail LIKE ? ", (email,))
                id_user = itemss.fetchall()
                itemss.execute(
                    "SELECT u.id_user FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.mail LIKE ?",
                    (email,))
                admin = itemss.fetchall()
                if len(admin) != 0:
                    session["admin"] = "oui"
                    itemss.execute(
                        "SELECT a.id_jardin FROM utilisateur u JOIN administre a ON u.id_user=a.id_user WHERE u.mail LIKE ?",
                        (email,))
                    num_jardin_a = itemss.fetchall()
                    session["num_jardin_a"] = enleveCrochets(num_jardin_a)
                session["id_user"] = id_user[0][0]
                itemss.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (id_user[0][0],))
                parc = itemss.fetchall()
                session["parcelles"] = enleveCrochets(parc)
                return redirect('/')
    return 'ERROR'


@app.route('/admin/nouvelle_parcelle')
def nouvelle_parcelle():
    if session['admin'] == 'oui':
        return render_template('admin/nouvelle_parcelle.html')
    else:
        return render_template('error_page.html', msg="Vous n'avez pas les droits d'administrateur")


@app.route('/send-creer-parcelle', methods=['POST', 'GET'])
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


@app.route('/admin/attribution_parcelles')
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


@app.route('/test')
def test():
    resultat = [[1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50]]],
                [1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50], [22, 1, 120, 50]]],
                [1, 37, 'rue Verlaine', 'Léo', [[22, 1, 120, 50]]]]
    return render_template('admin/attribution_parcelle.html', resultat=resultat)


"""
@app.route('/monpotager/<numero>')
def mon_potager(numero):
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    database = get_db()

    item = database.cursor()
    commande = "Select nom, prenom From utilisateur WHERE id_user = ?"
    item.execute(commande, (numero,))
    resultat = item.fetchall()

    if len(resultat) != 1:
        return 'error ce numero n\'est pas correct'
    nom, prenom = resultat[0]

    id_image = numero

    A = np.array([[0 for j in range(1000)] for i in range(500)])

    PotagerImage = image_py.PotagerImage(A, id_image, database.cursor())
    l_polynomes_txt, chemin_image = PotagerImage.html_code()
    l_legende = [('blue', 10), ('green', 11)]
    chemin = "potager_user/potager_user_affichage.html"

    print(chemin_image)
    return render_template(chemin, l_polynomes_txt=l_polynomes_txt[::-1], chemin_image=chemin_image, prenom=prenom,
                           l_legende=PotagerImage.legende(database.cursor()))
"""


# affichage de toutes les parcelles
@app.route('/mesparcelles')
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

        parametres.append([l_polynomes_txt, l_legende, chemin_image, id_parcelle, id_jardin])

    chemin = "potager_user/potager_user_affichage_global.html"
    return render_template(chemin, parametres=parametres)


# affichage individuel des parcelles (fonction d'ajout de plantes à mettre)
@app.route('/monpotager/<numero>')
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

    #vérifie que l'utilisateur a bien accès à cette parcelle (et qu'il a pas triché)
    cestpasbon=True
    for num in session.get("parcelles"):
        if num==numero:
            cestpasbon=False
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
    l_polygone = tp.string_to_lists(l_polygone)
    l_id = tp.string_to_lists(l_id)

    longueur, largeur = round(longueur), round(largeur)

    l_polygone_txt, chemin_image = image_py.html_code_fonction(l_polygone, l_id, id_parcelle)

    chemin_image = image_py.affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id,
                                               database.cursor())

    chemin = "potager_user/potager_user_affichage_individuel.html"
    print(chemin_image)

    return render_template(chemin, l_polynomes_txt=l_polygone_txt[::-1], chemin_image=chemin_image,
                           l_legende=image_py.legende_fonction(database.cursor(), l_id), numero=numero, id_jardin=id_jardin)


@app.route('/id_plante/<numero>')
def id_plante(numero):
    return numero


@app.route('/user/vos_informations')
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
    items.execute('SELECT nom, prenom, mail FROM utilisateur WHERE id_user = ?', (session.get("id_user"),))
    resultat = items.fetchall()[0]

    if items == []:
        return 'La page demandé n\'existe pas'

    donnees = {
        'lastname': resultat[0],
        'firstname': resultat[1],
        'email': resultat[2]
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

    if session['admin']=='oui':
        jardins=[]
        for i in session.get('num_jardin_a'):
            items = db.cursor()
            items.execute('SELECT j.id_jardin, j.code_postal, j.ville, j.numero_rue, j.nom_rue, j.id_referent, u.prenom, u.nom FROM jardin j JOIN utilisateur u ON u.id_user=j.id_referent WHERE id_jardin = ?', (i,))
            jardins.append(items.fetchall()[0])
                    
        
    return render_template('potager_user/user_page.html', donnees=donnees, parcelles=parcelles, jardins=jardins)


@app.route('/monpotager/<numero>/edit')
def edit_potager(numero):
    try:
        numero = int(numero)
    except:
        return 'error ce numero n\'est pas correct'

    return render_template('potager_user/edit_potager.html')


if __name__ == '__main__':
    app.run(debug=True)
