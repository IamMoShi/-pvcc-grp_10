"""
Le but de ce script est d\'ajouter, si cela est possible, une plante, en fonction de sa taille,
à l'endroit demandé et si cela est possible
"""
import numpy as np


def modification_terrain(terrain: np.array, taille_plante: int, position: tuple, id_plante: int):
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


def ajout_plante(terrain: np.array, taille_plante: int, position: tuple, id_plante: int, echelle=1):
    """
    :param terrain: matrice représentant le terrain, que l'on suppose non nulle
    car créé par la fonction de création de terrain
    :param taille_plante: on représente une plante par un carré de coté taille_plante, taille plante est un entier
    :param position: position du coin en haut à gauche de la plante, l'indice du jardin commence en 0,0
    :param id_plante: numéro d'identification de la plante (entier positif)
    :param echelle: xargs de valeur par défault
    :return:
    """
    taille_plante = int(taille_plante // echelle)
    print(taille_plante)
    if len(position) != 2:
        msg = 'Les coordonnées de position ne se pas correcte, cf taille tuple'
        return terrain, False, msg
    if position[0] < 0 or position[1] < 0:
        msg = 'position impossible car l\'une des coordonées est négative '
        return terrain, False, msg
    if position[0] + taille_plante > len(terrain[0]) or position[1] + taille_plante > len(terrain[1]):
        msg = 'La plante ne rentre pas dans le jardin à cette postion'
        return terrain, False, msg
    terrain_modifie = modification_terrain(terrain, taille_plante, position, id_plante)
    if terrain_modifie[0]:
        return terrain_modifie[1]
    else:
        return terrain
