import numpy as np

"""
direction : 4 valeurs :
- 1 : i += 1
- 2 : i += -1
- 3 : j += 1
- 4 : j += -1
"""


def give_direction(i, j, a, b):
    if a - i == 1:
        return 1
    if a - i == -1:
        return 2
    if b - j == 1:
        return 3
    if b - j == -1:
        return 4


def sides(i, j, longueur, largeur):
    cotes = []
    if i > 0:
        cotes.append((i - 1, j))
    if j > 0:
        cotes.append((i, j - 1))
    if i < longueur - 1:
        cotes.append((i + 1, j))
    if j < largeur - 1:
        cotes.append((i, j + 1))
    return cotes


def previous_elt(i, j, direction):
    if direction == 1:
        return i - 1, j
    if direction == 2:
        return i + 1, j
    if direction == 3:
        return i, j - 1
    if direction == 4:
        return i, j + 1


def next_in_raw_elt(i, j, direction):
    if direction == 1:
        return i + 1, j
    if direction == 2:
        return i - 1, j
    if direction == 3:
        return i, j + 1
    if direction == 4:
        return i, j - 1


def inside_elt(i, j, tableau_potager, longueur, largeur):
    id_plante = tableau_potager[i, j]
    cotes = sides(i, j, longueur, largeur)
    same = 0
    for k in cotes:
        if tableau_potager[k[0], k[1]] == id_plante:
            same += 1
    if same == 4:
        return True
    return False


def turn_left(direction):
    dico = {1: 3, 2: 4, 3: 2, 4: 1}
    return dico[direction]


def turn_right(direction):
    dico = {1: 4, 2: 3, 3: 1, 4: 2}
    return dico[direction]


def next_inside_elt(i, j, direction):
    """
    On sait que l'on va devoir tourner à droite,
     on demande donc à la fonction quelle est la direction vers la droite,
     puis un calcul l\'elt suivant dans cette direction et on le renvoie.
    On sait de plus que si l'on tourne à droite, c'est que les 4 côtés sont identiques,
    on ne se situe ainsi pas sur un bord.
    """
    direction = turn_right(direction)
    return next_in_raw_elt(i, j, direction), direction


def next_elt(i, j, tableau_potager, longueur, largeur, direction, id_plante) -> (int, int, int):
    """
    On doit savoir dans quel cas on se trouve. On traitera les cas par ordre d'importance
    Par exemple, si l'on est sur un coin où l'on doit tourner à droite,
    l'elt suivant a le même id que celui sur lequel on se trouve.
    On doit donc commencer par ce cas avant de traiter le cas où l'on avance tout droit
    """
    """
    On ne différencie pas un elt à l'intérieur d'un coin où l'on tourne à droite
    """
    if inside_elt(i, j, tableau_potager, longueur, largeur):
        x, y = next_inside_elt(i, j, direction)
        a, b = x
        return a, b, y

    """
    On test à présent l'elt suivant en suivant la même direction
    a, b sont les coordonnées de se point,
    il faut tout d'abord vérifier qu'il existe, et si c'est le cas alors il faut continuer tout droit
    """
    a, b = next_in_raw_elt(i, j, direction)
    if 0 <= a < longueur and 0 <= b < largeur and tableau_potager[a, b] == id_plante:
        return a, b, direction

    """
    Ici on ne peut plus aller tout droit ni tourner à droite, il faut donc ... tourner à gauche non ?
    On change la direction pour que l'on soit vers la gauche et ensuite on calcul l'elt suivant
    """

    direction = turn_left(direction)
    a, b = next_in_raw_elt(i, j, direction)
    return a, b, direction


def bordure_penible(couple_bordure, direction, a, b):
    """
    It's kind of magic
    """
    if direction == 1 or direction == 4:
        if couple_bordure == (0, 0):
            return (0, 0), [(a, b)]
        if couple_bordure == (1, 0):
            return (0, 0), []
        if couple_bordure == (1, 1):
            return (0, 0), [(a, b + 2), (a, b + 1), (a, b)]

    if direction == 3:
        if couple_bordure == (0, 0):
            return (1, 0), [(a + 1, b - 1), (a + 1, b)]
        if couple_bordure == (1, 0):
            return (1, 0), [(a + 1, b)]
        if couple_bordure == (1, 1):
            return (1, 0), []

    if direction == 2:
        if couple_bordure == (0, 0):
            return (1, 1), []
        if couple_bordure == (1, 0):
            return (1, 1), [(a + 2, b + 1), (a + 1, b + 1)]
        if couple_bordure == (1, 1):
            return (1, 1), [(a + 1, b + 1)]


def outline(i, j, tableau_potager, longueur, largeur):
    """
    :param i: position du premier coin de notre contour
    :param j: position du premier coin de notre contour
    :param tableau_potager: le potager sous forme de matrice numpy 2D avec laquelle on travaille
    :param longueur: longueur de ce tableau
    :param largeur: largeur de ce tableau
    :return: liste de couple (a, b) de position "dans" ce tableau
    On va progresser point par point en calculant le prochain point de notre contour,
    par contre on n'ajoutera pas forcément ce point à notre liste de point du contour
    puisque l'on veut le contour compris dans notre polygone (pas comme dans la v1 de ce programme).
    """
    id_plante = tableau_potager[i, j]
    """
    On commence par crée la liste des points du contour qui s'appelle contour et qui contient des couples (a, b).
    On sait de plus que le point (i, j) fait parti de ce contour.
    Contour compris est la nuance de contour mais avec les elts manquant de la version 1 de ce prgm
    """
    contour = [(i, j)]
    contour_compris = [(i, j)]
    """
    La première direction d'exploration est 1 comme cela on tournera dans le sens trigonométrique
    et les propriétés des fonctions de calcul des elts suivant sont vraies
    """
    direction = 1
    """
    On doit à present continuer d'explorer ce contour jusqu'à ce que l'on retombe sur nos pieds
    on comptera le nombre de tour de boucle avec i
    """
    k = 0
    a, b = i, j
    couple_bordure = (0, 0)
    while a != i or b != j or k == 0:
        a, b, direction = next_elt(a, b, tableau_potager, longueur, largeur, direction, id_plante)
        contour.append((a, b))
        if couple_bordure == (0, 0) and direction == 2:
            contour_compris.pop(-1)  # On est allé trop loin Maurice
        couple_bordure, ajout = bordure_penible(couple_bordure, direction, a, b)  # De la magie je vous dis
        contour_compris.extend(ajout)
        k += 1

    return contour, contour_compris


def solve_outlines(tableau_potager):
    longueur, largeur = tableau_potager.shape
    l_contours = []
    l_contours_compris = []
    l_id = []
    for x in range(longueur):
        for y in range(largeur):

            if not inside_elt(x, y, tableau_potager, longueur, largeur):
                id_plante = tableau_potager[x, y]
                if id_plante not in l_id:
                    l1, l2 = outline(x, y, tableau_potager, longueur, largeur)
                    l_contours.append(l1)
                    l_contours_compris.append(l2)
                    l_id.append(id_plante)
                else:
                    trouve = False
                    for contour in l_contours:
                        for k in contour:
                            if (x, y) == k:
                                trouve = True
                                break
                    if not trouve:
                        l1, l2 = outline(x, y, tableau_potager, longueur, largeur)
                        l_contours.append(l1)
                        l_contours_compris.append(l2)
    return l_contours_compris


def simplify(l_contours):
    l_contours_simplifie = []

    for contour in l_contours:
        contour_simplifie = [contour[0]]
        len_contour = len(contour)
        direction = 1

        for k in range(1, len_contour):
            a, b = contour[k - 1]
            x, y = contour[k]
            if direction != give_direction(a, b, x, y):
                contour_simplifie.append(contour[k - 1])
                direction = give_direction(a, b, x, y)

        l_contours_simplifie.append(contour_simplifie)
    return l_contours_simplifie


def resize_liste(l_polygones, k: int):
    def resize(liste_couples):
        liste_couples_redimensionnees = []
        for couple in liste_couples:
            liste_couples_redimensionnees.append((couple[0] * k, couple[1] * k))
        return liste_couples_redimensionnees

    l_polygones_redimensionnes = []
    i = 0
    while i < len(l_polygones):
        l_polygones_redimensionnes.append(resize(l_polygones[i]))
        i += 1
    return l_polygones_redimensionnes


def reverse(l_polynomes):
    l_liste = []
    for polynome in l_polynomes:
        liste = []
        for couple in polynome:
            liste.append((couple[1], couple[0]))
        l_liste.append(liste)
    return l_liste

