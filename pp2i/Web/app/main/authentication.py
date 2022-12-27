from flask import Blueprint, render_template, redirect, session, request

from ..fonctions.login import hash as hash_py
from ..fonctions.login import register as register_py
from ..fonctions.login import signin as signin_py
from ..database.get_db import get_db
from ..fonctions.main.enleve_crochets import enleve_crochets

authentication = Blueprint('authentication', __name__)


@authentication.route('/signin')
def signin():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return render_template("login/login.html", b_signin=True, b_register=False)


@authentication.route('/register')
def signup():
    return render_template("login/login.html", b_signin=False, b_register=True)


@authentication.route('/login')
def login():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return render_template("login/login.html", b_signin=True, b_register=True)


@authentication.route('/logout')
def logout():
    session["email"] = None
    session["name"] = None
    session["id_user"] = None
    session["admin"] = None
    session["num_jardin_a"] = None
    session["parcelles"] = None
    return redirect("/")


@authentication.route('/send-register-form', methods=['POST', 'GET'])
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


@authentication.route('/send-signin-form', methods=['POST', 'GET'])
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
                    session["num_jardin_a"] = enleve_crochets(num_jardin_a)
                session["id_user"] = id_user[0][0]
                itemss.execute("SELECT id_parcelle FROM parcelle WHERE id_user LIKE ?", (id_user[0][0],))
                parc = itemss.fetchall()
                session["parcelles"] = enleve_crochets(parc)
                return redirect('/')
    return 'ERROR'
