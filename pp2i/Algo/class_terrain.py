import numpy as np

'''
Création de l'objet Terrain regroupant un ensemble de fonction applicable sur un terrain
Ceci n'est que le début de la création de l'objet Terrain, il sera nécessaire d'ajouter des fonctionnalités !
'''


class Terrain:
    """
    :parameter: var
        :param longueur: représente l'une des dimensions en cm du jardin, nombre réel positif
        :param largeur:  représente l'autre dimension en cm du jardin
        :param echelle: représente l'échelle à laquelle la matrice va être crée (cm), valeur par default = 1cm
    :parameter: func
        __init__ : dimension_terrain as a tuple
            needed to create the array Mon_tableau
        modification_echelle : change de scale of mon_terrain,
            must be used before creating mon_terrain

    """

    echelle = 1
    longueur, largeur = 0, 0
    mon_terrain = np.array([])
    data_terrain = dict({
        'dimensions': (longueur, largeur)
    })

    def __init__(self, dimensions_terrain: tuple):
        """
        :param dimensions_terrain : définit la taille de l'un des jardins
                couple de valeur entière en cm
        """

        if len(dimensions_terrain) != 2:
            print('Erreur de dimension du tuple dimension_terrain')
            exit()
        if dimensions_terrain[0] <= 0 or dimensions_terrain[1] <= 0:
            print('Error dimensions must be positive')
        self.longueur, self.largeur = dimensions_terrain
        self.data_terrain.update(dimension=dimensions_terrain)

    def modification_echelle(self, echelle: float):
        """
        :param echelle: modifie l'échelle de la matrice qui est par default de 1cm par elt
        :return: retourne et modifie juste la valeur de l'échelle de l'objet
        """
        if not np.array_equal(self.mon_terrain, []):
            return 'une matrice représentant le terrain existe déjà, échelle actuelle : ' + str(self.echelle)
        if type(echelle) != float:
            return 'erreur type echelle'
        if echelle <= 0:
            return 'echelle is negative or null'
        self.echelle = echelle
        return self.echelle

    def creation_terrain(self):
        """
        :return: retourne une matrie (np.array)
        dont les dimensions sont retranscrites par l'échelle en un nombre de colonne dans la matrice,
        un booléen représentant le succès de l'opération et aussi un message,
        on se concentre sur la création d'un terrain rectangulaire
        """

        if self.longueur < 0:
            self.longueur = -self.longueur
            self.creation_terrain()  # auto adaptation aux valeurs négatives
        if self.longueur == 0:
            msg = 'longueur nulle'
            return np.array([]), False, msg
        if self.largeur < 0:
            self.largeur = -self.largeur
            self.creation_terrain()
        if self.largeur == 0:
            msg = 'largeur nulle'
            return np.array([]), False, msg

        self.longueur = int(self.longueur // self.echelle)  # adaptation à l'échelle
        self.largeur = int(self.largeur // self.echelle)

        try:
            # création d'une matrice de -1 de la taille demandé par mise à l'échelle
            self.mon_terrain = np.full((self.longueur, self.largeur), -1)
            msg = 'opération réussie'
            return self.mon_terrain, True, msg
        except (Exception,):
            # cas d'erreur inconnue dans la création du tableau
            msg = 'erreur dans la fonction '
            return np.array([]), False, msg

    def modification_terrain(self, terrain: np.array, taille_plante: int, position: tuple, id_plante: int):
        """
        :param terrain: prend un terrain (utilisé pour ne pas modifier Mon_terrain, la matrice de l'objet Terrain
        :param taille_plante: taille plante est supposé être la longueur du côté du carré necessaire à la plante
        :param position: position en partant de en haut à gauche de la plante dans le jardin (init : (0,0)
        :param id_plante: identifiant unique de la plante à placer selon son type, doit être positif
        :return: Booléen représentant le succès de la modification et le terrain modifié
        """
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
        :return: le terrain modifié si la modification était possible,
            le booléen représentant le succès de la modification
            et un message associé à la modification (pour le debug)
        """
        taille_plante = int(taille_plante // self.echelle)
        if len(position) != 2:
            msg = 'Les coordonnées de position ne se pas correcte, cf taille tuple'
            return self.mon_terrain, False, msg

        if position[0] < 0 or position[1] < 0:
            msg = 'position impossible car l\'une des coordonnées est négative '
            return self.mon_terrain, False, msg

        if position[0] + taille_plante > len(self.mon_terrain[0]) \
                or position[1] + taille_plante > len(self.mon_terrain[1]):
            msg = 'La plante ne rentre pas dans le jardin à cette position'
            return self.mon_terrain, False, msg

        terrain_modifie = self.modification_terrain(self.mon_terrain, taille_plante, position, id_plante)

        if terrain_modifie[0]:
            self.mon_terrain = terrain_modifie[1]
            msg = 'Ajout réussi'
            return self.mon_terrain, True, msg
        else:
            msg = 'problème d\'ajout'
            return self.mon_terrain, False, msg

    def colorisation(self):
        '''
        fonction dédiée à l'affichage web du terrain en remplaçant les id par des couleurs
        :return: une matrice n, p avec des codes couleurs du type b'xxxxxx' avec x un int en base 10
        '''

        def couleur(nombre):
            if nombre == -1:
                return '#202020'
            str_num = '#' + str(((nombre) * 123) % 10 ** 7)
            for k in range(7 - len(str_num)):
                str_num = str_num + '0'
            return str_num

        longeur_ligne, longeur_colonne = np.shape(self.mon_terrain)
        mon_terrain_colorie = np.chararray((longeur_ligne, longeur_colonne), itemsize=7)

        for i in range(longeur_ligne):
            for j in range(longeur_colonne):
                x = self.mon_terrain[i, j]
                mon_terrain_colorie[i, j] = couleur(x)
        return mon_terrain_colorie
