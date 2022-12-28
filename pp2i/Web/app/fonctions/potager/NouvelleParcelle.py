import numpy as np
import sys
from os.path import dirname

sys.path.append(dirname(__file__))
from .reverse import reverse
from .resize_liste import resize_liste


class NouvelleParcelle:
    alpha = 2  # redimensionnement des coefficients de la matrice en px
    file = 'static/images/images_potagers/'

    def __init__(self, longueur, largeur):
        self.longueur = longueur
        self.largeur = largeur
        self.tableau_potager = np.zeros((longueur, largeur))

        l_polygones = [[(0, 0), (largeur + 1, 0), (largeur + 1, longueur + 1), (0, longueur + 1)]]

        # Pour utiliser la fonction area et par la création de l'image, on doit inverser i et j.
        l_polygones = reverse(l_polygones)

        # On garde le contour en mémoire dans l'objet
        self.l_contours = l_polygones

        # On le redimensionne afin d'avoir une image plus grande
        l_polygones = resize_liste(l_polygones, self.alpha)

        # On garde le contour agrandi
        self.l_polygones = l_polygones

    def l_polygones(self):
        return self.l_polygones
