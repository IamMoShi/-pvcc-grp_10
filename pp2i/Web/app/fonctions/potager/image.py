import numpy as np
from PIL import Image, ImageDraw
import sys
from os.path import dirname

sys.path.append(dirname(__file__))
import transformation_polygone_v2 as tp


class PotagerImage:
    alpha = 2  # redimensionnement des coefficients de la matrice en px
    file = 'static/images/images_potagers/'

    def __init__(self, tableau_potager, id_image, items):
        # Récupération des données propres à l'objet
        self.size = (len(tableau_potager[0]) * self.alpha, len(tableau_potager) * self.alpha)
        self.tableau_potager = tableau_potager
        self.id_image = id_image

        # Récupération des contours générés par l'algo transformation polygone_v2
        l_contours, self.l_id = tp.solve_outlines(tableau_potager)

        # On simplifie les contours pour ne garder que les sommets
        l_polygones = tp.simplify(l_contours)

        # Pour utiliser la fonction area et par la création de l'image, on doit inverser i et j.
        l_polygones = tp.reverse(l_polygones)

        # On garde le contour en mémoire dans l'objet
        self.l_contours = l_polygones

        # On le redimensionne afin d'avoir une image plus grande
        l_polygones = tp.resize_liste(l_polygones, self.alpha)

        # On garde le contour agrandi
        self.l_polygones = l_polygones

        """
        On colorie l'image à l'aide des polygones que l'on a obtenus dans la partie précédente du programme
        Si la valeur est 0 alors il n'y a pas de plante, on laisse en gris, 
        Sinon on va voir dans la base de donnée la couleur associé à la plante
        """

        creation_image(l_polygones, tableau_potager, self.alpha, items, self.file, self.id_image)

    def polygone(self):
        """
        Cette fonction à pour but de récupérer les polygones décrivant le terrain afin de facilité la sauvegarde
        On récupère la liste des polygones pour la sauvegarder dans la base de données et réduire le temps execution
        :return: liste des contours sans redimensionnement, liste des contours redimensionnés
        """
        return self.l_contours, self.l_polygones, self.alpha

    def image_path(self):
        """
        :return: str : le chemin où se trouve l'image créée lors de la création de l'objet
        """
        return self.file + str(self.id_image) + '.png'

    def html_code(self):
        return html_code_fonction(
            self.l_polygones,
            self.l_id,
            self.id_image,
            self.file)

    def legende(self, items):
        return legende_fonction(items, self.l_id)


class NouvelleParcelle:
    alpha = 2  # redimensionnement des coefficients de la matrice en px
    file = 'static/images/images_potagers/'

    def __init__(self, longueur, largeur):
        self.longueur = longueur
        self.largeur = largeur
        self.tableau_potager = np.zeros((longueur, largeur))

        l_polygones = [[(0, 0), (largeur + 1, 0), (largeur + 1, longueur + 1), (0, longueur + 1)]]

        # Pour utiliser la fonction area et par la création de l'image, on doit inverser i et j.
        l_polygones = tp.reverse(l_polygones)

        # On garde le contour en mémoire dans l'objet
        self.l_contours = l_polygones

        # On le redimensionne afin d'avoir une image plus grande
        l_polygones = tp.resize_liste(l_polygones, self.alpha)

        # On garde le contour agrandi
        self.l_polygones = l_polygones

    def l_polygones(self):
        return self.l_polygones


def affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id, items,
                       id_user=None, file='static/images/images_potagers/'):
    print('hello')
    creation_image_by_id(l_polygone, l_id, (longueur, largeur), items, file, id_parcelle)
    return file + str(id_parcelle) + '.png'


def html_code_fonction(l_polygones, l_id, id_image=0, file=''):
    """
    :return: (list[str], str), change le formatage de l'information contenue dans l_polygone pour facilité
    la lecture dans le fichier html
    Donne l'endroit où se trouve l'image correspondante à l'objet
    """
    l_polygones_txt = tp.to_text(l_polygones, l_id)
    chemin_image = "/" + file + str(id_image) + '.png'
    return l_polygones_txt, chemin_image


def legende_fonction(items, l_id):
    """
    :param: items : cursor de la database
    :return: la liste des couleurs et des noms associées à chaque plante présente dans le jardin
    """
    l_legende = [('grey', 0)]
    l_id = []

    for id in l_id:
        items.execute('select color from plante where id_plante = ?', (int(id),))
        result = items.fetchall()
        if len(result) == 1 and id not in l_id:
            l_id.append(id)
            l_legende.append((result[0][0], id))
    return l_legende


def creation_image(l_polygones, tableau_potager, alpha, items, file, id_image):
    # Création de l'esquisse que l'on va peindre par la sutie
    size = (len(tableau_potager[0]) * alpha, len(tableau_potager) * alpha)
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img, mode='RGB')


    for polygone in l_polygones:
        id_plante = tableau_potager[(polygone[0][1] // alpha, polygone[0][0] // alpha)]

        if id_plante == 0:
            draw.polygon(polygone, fill='grey', width=1, outline=None)
        else:
            items.execute('select color from plante where id_plante = ?', (int(id_plante),))
            color = int(items.fetchall()[0][0])
            draw.polygon(polygone, fill=color, width=1, outline=None)

    img.save(file + str(id_image) + '.png', "PNG")


def creation_image_by_id(l_polygones, l_id, size, items, file, id_image):
    # Création de l'esquisse que l'on va peindre par la suite
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img, mode='RGB')
    i = 0
    for polygone in l_polygones:
        id_plante = l_id[i]
        i += 1

        if id_plante == 0:
            draw.polygon(polygone, fill='grey', width=1, outline=None)
        else:
            items.execute('select color from plante where id_plante = ?', (int(id_plante),))
            color = items.fetchall()[0][0]
            draw.polygon(polygone, fill=color, width=1, outline=None)

    img.save(file + str(id_image) + '.png', "PNG")
