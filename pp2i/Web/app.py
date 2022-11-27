from flask import Flask, render_template, request, redirect, g
import back_python.login.register as register_py
import back_python.login.signin as signin_py
import back_python.login.hash as hash_py
import back_python.potager.image as image_py
import sqlite3
import numpy as np

app = Flask(__name__)

DATABASE = 'database/database.db'


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
    return render_template("login/login.html", b_signin=True, b_register=False)


@app.route('/register')
def signup():
    return render_template("login/login.html", b_signin=False, b_register=True)


@app.route('/login')
def login():
    return render_template("login/login.html", b_signin=True, b_register=True)


@app.route('/users')
def users():
    db = get_db()
    items = db.cursor()
    items.execute("SELECT * FROM utilisateur")
    data = items.fetchall()
    return render_template("login/users.html", data=data)


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
            return 'POST'
    return 'ERROR'


@app.route('/send-signin-form', methods=['POST', 'GET'])
def signin_post():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if signin_py.signin(email, password):
            print(password)
            pwd_hash = hash_py.hash(password)
            db = get_db()
            items = db.cursor()
            items.execute("SELECT count(*) FROM utilisateur WHERE mail LIKE ? and mdp = ? ", (email, pwd_hash,))
            if len(items.fetchall()[0]) != 1:
                return 'Le mdp ou l\'email sont incorect'

            return 'Connected'
    return 'ERROR'


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
    A = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    A = np.array([[0 for j in range(1000)] for i in range(500)])

    PotagerImage = image_py.PotagerImage(A, id_image, database.cursor())
    l_polynomes_txt, chemin_image = PotagerImage.html_code()
    l_legende = [('blue', 10), ('green', 11)]
    chemin = "potager_user/potager_user_affichage.html"

    print(chemin_image)
    return render_template(chemin, l_polynomes_txt=l_polynomes_txt[::-1], chemin_image=chemin_image, prenom=prenom,
                           l_legende=PotagerImage.legende(database.cursor()))


@app.route('/id_plante/<numero>')
def id_plante(numero):
    return numero


if __name__ == '__main__':
    app.run(debug=True)
