import sys
from os.path import dirname

sys.path.append(dirname(__file__))
from .transformation_polygone_v2 import *
from .simplify import simplify
from .reverse import reverse
from .resize_liste import resize_liste
from .creation_image import creation_image
from .html_code_fonction import html_code_fonction
from .legende_fonction import legende_fonction


class PotagerImage:
    alpha = 2  # redimensionnement des coefficients de la matrice en px
    file = 'static/images/images_potagers/'

    def __init__(self, tableau_potager, id_image, items):
        # Récupération des données propres à l'objet
        self.size = (len(tableau_potager[0]) * self.alpha, len(tableau_potager) * self.alpha)
        self.tableau_potager = tableau_potager
        self.id_image = id_image

        # Récupération des contours générés par l'algo transformation polygone_v2
        l_contours, self.l_id = solve_outlines(tableau_potager)

        # On simplifie les contours pour ne garder que les sommets
        l_polygones = simplify(l_contours)

        # Pour utiliser la fonction area et par la création de l'image, on doit inverser i et j.
        # l_polygones = reverse(l_polygones)
        #print(l_polygones)
        # On garde le contour en mémoire dans l'objet
        self.l_contours = l_polygones

        # On le redimensionne afin d'avoir une image plus grande
        l_polygones = resize_liste(l_polygones, self.alpha)

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
