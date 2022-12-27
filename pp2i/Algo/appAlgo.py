from flask import Flask, render_template, request, redirect
import class_terrain

terrain = class_terrain.Terrain((60, 100))

app = Flask(__name__)


@app.route('/status')
def index():
    return ('Up and Running')


@app.route('/test')
def test():
    mon_terrain = terrain.creation_terrain()
    mon_terrain, B, msg = terrain.ajout_plante(16, (0, 0), 1)
    mon_terrain, B, msg = terrain.ajout_plante(20, (10, 30), 2)
    mon_terrain, B, msg = terrain.ajout_plante(12, (50, 15), 3)
    mon_terrain, B, msg = terrain.ajout_plante(18, (25, 2), 5)
    mon_terrain, B, msg = terrain.ajout_plante(10, (26, 3), 7)
    print(msg)
    mon_terran_colorie = terrain.colorisation()
    return render_template('test.html', matrice = mon_terran_colorie)


if __name__ == '__main__':
    app.run(debug=True)
