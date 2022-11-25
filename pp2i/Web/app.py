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


@app.route('/navbar')
def navbar():
    return render_template("navBar.html")


@app.route('/signin')
def signin():
    return render_template("login/signin.html")


@app.route('/signup')
def signup():
    return render_template("login/signup.html")


@app.route('/login')
def login():
    return render_template("login/login.html")


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

            if items.fetchall()[0] != 1:
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
            if items.fetchall()[0][0] != 1:
                return 'Le mdp ou l\'email sont incorect'

            return 'Connected'
    return 'ERROR'


@app.route('/test')
def test():
    A = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    database = get_db()
    id_image = 10
    PotagerImage = image_py.PotagerImage(A, id_image, database.cursor())
    return 'fait'


if __name__ == '__main__':
    app.run(debug=True)
