"""
Le but de ce script est d\'ajouter, si cela est possible, une plante, en fonction de sa taille, à l'endroit demandé et si cela est possible
"""

def modification_terrain(terrain : array, taille : int, position : tuple):

    return

def ajout_plante(terrain : array, taille_plante : int, position : tuple):
    """
    :param terrain: matrice représentant le terrain
    :param taille_plante: on représente une plante par un carré de coté taille_plante, taille plante est un entier
    :param position: position du coin en haut à gauche de la plante, l'indice du jardin commence en 0,0
    :return:
    """
    if len(position) != 2:
        msg = 'Les coordonnées de position ne se pas correcte, cf taille tuple'
        return terrain, False, msg
    if position[0] < 0 or position[1] < 0:
        msg = 'position impossible car l\'une des coordonées est négative'
        return terrain, False, msg
    if position[0] + taille_plante >= len(terrain[0]) or position[1] + taille_plante >= len(terrain[1]):
        msg = 'La plante ne rentre pas dans le jardin à cette postion'
        return terrain, False, msg




