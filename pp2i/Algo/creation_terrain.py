import numpy as np



def creation_terrain(longueur: float, largeur: float, echelle=1):
    """
    :param longueur: représente l'une des dimensions en cm du jardin, nombre réel positif
    :param largeur:  représente l'autre dimension en cm du jardin
    :param echelle: représente l'échelle à laquelle la matrice va être crée (cm), valeur par défault = 1cm
    :return: retourne une matrie (np.array) dont les dimensions sont retranscrite par l'echelle en un nombre de colonne dans la matrice, un booléen représentant le succès de l'opération et aussi un message
    on se concentre sur la création d'un terrain rectangulaire
    """

    if longueur < 0:
        return creationTerrain(-longueur, largeur)
    if longueur == 0:
        msg = 'longueur nulle'
        return np.array([]), False, msg
    if largeur < 0:
        return creationTerrain(longueur, -largeur)
    if largeur == 0:
        msg = 'largeur nulle'
        return np.array([]), False

    longueur = round(longueur)
    largeur = round(largeur)

    try:
        mon_terrain = np.full((longueur, largeur), '-1')
        msg = 'opération réussie'
        return mon_terrain, True, msg
    except:
        msg = 'erreur dans la fonction '
        return np.array([]), False, msg

print(creation_terrain(10,20))