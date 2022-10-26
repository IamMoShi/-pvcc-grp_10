import numpy as np


class Terrain:
    """
    :parameter: var
        :param longueur: représente l'une des dimensions en cm du jardin, nombre réel positif
        :param largeur:  représente l'autre dimension en cm du jardin
        :param echelle: représente l'échelle à laquelle la matrice va être crée (cm), valeur par default = 1cm
    :parameter: func
        __init__ : dimension_terrain

    """

    echelle = 1
    longueur, largeur = 0, 0
    mon_terrain = np.array([])

    def __init__(self, dimension_terrain: tuple):
        """
        :param dimension_terrain: definit la taille de l'un des jardin
                couple de valeur entière en cm
        """
        if len(dimension_terrain) != 2:
            print('Erreur de dimension du tuple dimension_terrain')
            exit()

        self.longueur, self.largeur = dimension_terrain

    def echelle(self, echelle):
        """
        :param echelle: modifie l'echelle de la matrice qui est par default de 1cm par elt
        :return: retourne et modifie juste la valeur de l'echelle de l'objet
        """
        self.echelle = echelle
        return self.echelle

    def creation_terrain(self):
        """
        :return: retourne une matrie (np.array)
        dont les dimensions sont retranscrites par l'echelle en un nombre de colonne dans la matrice,
        un booléen représentant le succès de l'opération et aussi un message,
        on se concentre sur la création d'un terrain rectangulaire
        """

        if self.longueur < 0:
            self.longueur = -self.longueur
            self.creation_terrain()
        if self.longueur == 0:
            msg = 'longueur nulle'
            return np.array([]), False, msg
        if self.largeur < 0:
            self.largeur = -self.largeur
            self.creation_terrain()
        if self.largeur == 0:
            msg = 'largeur nulle'
            return np.array([]), False

        self.longueur = int(self.longueur // self.echelle)
        self.largeur = int(self.largeur // self.echelle)

        try:
            self.mon_terrain = np.full((self.longueur, self.largeur), '-1')
            msg = 'opération réussie'
            return self.mon_terrain, True, msg
        except:
            msg = 'erreur dans la fonction '
            return np.array([]), False, msg

    def modification_terrain(self, terrain: np.array, taille_plante: int, position: tuple, id_plante: int):
        x, y = position
        colonne_legume = np.full_like(np.zeros(taille_plante), id_plante)
        colonne_vide = np.full_like(np.zeros(taille_plante), -1)
        for k in range(taille_plante):
            if np.array_equal(
                    terrain[y + k, x:x + taille_plante],
                    colonne_vide
            ):
                terrain[y + k, x:x + taille_plante] = colonne_legume
            else:
                return False, terrain
        return True, terrain

    def ajout_plante(self, taille_plante: int, position: tuple, id_plante: int):
        """
        :param taille_plante: on représente une plante par un carré de coté taille_plante, taille plante est un entier
        :param position: position du coin en haut à gauche de la plante, l'indice du jardin commence en 0,0
        :param id_plante: numéro d'identification de la plante (entier positif)
        :return:
        """
        taille_plante = int(taille_plante // self.echelle)
        if len(position) != 2:
            msg = 'Les coordonnées de position ne se pas correcte, cf taille tuple'
            return self.mon_terrain, False, msg

        if position[0] < 0 or position[1] < 0:
            msg = 'position impossible car l\'une des coordonées est négative '
            return self.mon_terrain, False, msg

        if position[0] + taille_plante > len(self.mon_terrain[0]) \
                or position[1] + taille_plante > len(self.mon_terrain[1]):
            msg = 'La plante ne rentre pas dans le jardin à cette postion'
            return self.mon_terrain, False, msg

        terrain_modifie = self.modification_terrain(self.mon_terrain, taille_plante, position, id_plante)

        if terrain_modifie[0]:
            self.mon_terrain = terrain_modifie[1]
            msg = 'Ajout réussi'
            return self.mon_terrain, True, msg
        else:
            msg = 'problème d\'ajout'
            return self.mon_terrain, False, msg
