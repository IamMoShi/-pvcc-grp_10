from flask import Flask, render_template, request, redirect
import class_terrain
import sqlite3

terrain = class_terrain.Terrain((100, 100))

app = Flask(__name__)


@app.route('/status')
def index():
    return ('Up and Running')


@app.route('/test')
def test():
    data = sqlite3.connect("../Web/database/database.db")
    mon_terrain = terrain.creation_terrain()
    cur = data.cursor()
    cur.execute("select id_plante,x_plante,y_plante from contient where id_parcelle like ?",(2,))
    result=cur.fetchall()
    for i in result:
        mon_terrain, B, msg = terrain.ajout_plante(20, (i[1], i[2]), i[0])
    mon_terran_colorie = terrain.colorisation()
    return render_template('test.html', matrice = mon_terran_colorie)

if __name__ == '__main__':
    app.run(debug=True)
