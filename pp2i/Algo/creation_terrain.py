'''
Cette page doit contenir l'agorithme permettant de créer le jardin que possède un utilisateur

Le jardin sera représenté par une matrice
Le choix de la taille d'une case de la matrice sera déterminé par la valeur prise par la constante echelle
'''
import numpy as np


def creation_terrain(longueur: float, hauteur: float, echelle=1):
    """
    :param longueur: représente l'une des dimensions en cm du jardin, nombre réel positif
    :param hauteur:  représente l'autre dimension en cm du jardin
    :param echelle: représente l'échelle à laquelle la matrice va être crée (cm), valeur par défault = 1cm
    :return: retourne une matrie (np.array) dont les dimensions sont retranscrite par l'echelle en un nombre de colonne dans la matrice, un booléen représentant le succès de l'opération et aussi un message
    on se concentre sur la création d'un terrain rectangulaire
    """

    if longueur < 0:
        return creationTerrain(-longueur, hauteur)
    if longueur == 0:
        msg = 'longueur nulle'
        return np.array([]), False, msg
    if hauteur < 0:
        return creationTerrain(longueur, -hauteur)
    if hauteur == 0:
        msg = 'hauteur nulle'
        return np.array([]), False

    longueur = round(longueur)
    hauteur = round(hauteur)

    try:
        mon_terrain = np.full((longueur, hauteur), None)
        msg = 'opération réussie'
        return mon_terrain, True, msg
    except:
        msg = 'erreur dans la fonction '
        return np.array([]), False, msg

print(creation_terrain(10,20))