from flask import Flask, render_template, request, redirect
import class_terrain
import sqlite3

terrain = class_terrain.Terrain((200, 300))

app = Flask(__name__)

@app.route('/status')
def index():
    return ('Up and Running')


@app.route('/test')
def test():
    data = sqlite3.connect("app/database/database.db")
    mon_terrain = terrain.creation_terrain()
    mon_terrain, B, msg = terrain.ajout_plante(20, (0, 0), 1)
    cur = data.cursor()
    cur.execute("select id_plante,x_plante,y_plante from contient where id_parcelle like ?",(93,))
    result=cur.fetchall()
    for i in result:
        cur.execute("select taille from plante where id_plante like ?",(i[0],))
        result2=cur.fetchall()
        mon_terrain, B, msg = terrain.ajout_plante(result2[0][0], (i[1], i[2]), i[0])
        if not B:
            cur.execute("delete from contient where x_plante like ? and y_plante like ? and id_parcelle like ?",(i[1],i[2],27,))
            data.commit()
    mon_terran_colorie = terrain.colorisation()
    return render_template('test.html', matrice = mon_terran_colorie)

if __name__ == '__main__':
    app.run(debug=True)