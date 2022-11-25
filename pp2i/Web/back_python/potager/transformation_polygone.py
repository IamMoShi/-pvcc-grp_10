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


def next_elt(i, j, tableau_potager, longueur, largeur, direction, id_plante):
    cotes = sides(i, j, longueur, largeur)

    interieur = 0
    for k in cotes:
        if tableau_potager[k[0], k[1]] == id_plante:
            interieur += 1
    if interieur == 4:
        cotes.remove(next_in_raw_elt(i, j, direction))
        a, b = previous_elt(i, j, direction)
        cotes.remove((a, b))

        cotes_precedent = sides(a, b, longueur, largeur)

        cotes_cotes_actuel = []

        for k in cotes:
            cotes_cotes_actuel = cotes_cotes_actuel + sides(k[0], k[1], longueur, largeur)
        for k in cotes_precedent:
            if tableau_potager[k[0], k[1]] != id_plante and k in cotes_cotes_actuel:
                direction = give_direction(a, b, k[0], k[1])
                a, b = next_in_raw_elt(i, j, direction)
                return a, b, direction

    a, b = next_in_raw_elt(i, j, direction)
    if 0 <= a < longueur and 0 <= b < largeur:
        if tableau_potager[a, b] == id_plante:
            return a, b, direction
        cotes.remove((a, b))

    cotes.remove(previous_elt(i, j, direction))
    for k in cotes:
        a, b = k
        if tableau_potager[a, b] == id_plante:
            direction = give_direction(i, j, a, b)
            return a, b, direction

    return 'error'


def outline(i, j, tableau_potager, longueur, largeur):
    id_plante = tableau_potager[i, j]
    elt_bord = [(i, j)]
    direction = 1
    a, b, direction = next_elt(i, j, tableau_potager, longueur, largeur, direction, id_plante)

    if direction == 5:
        return 'error'

    elt_bord.append((a, b))
    while a != i or b != j:
        a, b, direction = next_elt(a, b, tableau_potager, longueur, largeur, direction, id_plante)
        elt_bord.append((a, b))

    return elt_bord


def solve_outlines(tableau_potager):
    longueur, largeur = tableau_potager.shape
    l_contours = []
    l_id = []
    for x in range(longueur):
        for y in range(largeur):
            if not inside_elt(x, y, tableau_potager, longueur, largeur):
                id_plante = tableau_potager[x, y]
                if id_plante not in l_id:
                    l_contours.append(outline(x, y, tableau_potager, longueur, largeur))
                    l_id.append(id_plante)
                else:
                    trouve = False
                    for contour in l_contours:
                        for k in contour:
                            if (x, y) == k:
                                trouve = True
                                break
                    if not trouve:
                        l_contours.append(outline(x, y, tableau_potager, longueur, largeur))
    return l_contours


def simplify(l_contours):
    l_contours_simplifie = []
    for contour in l_contours:
        contour_simplifie = [contour[0]]
        i = 1
        while i < len(contour) - 1:
            dir1 = give_direction(contour[i][0], contour[i][1], contour[i - 1][0], contour[i - 1][1])
            dir2 = give_direction(contour[i + 1][0], contour[i + 1][1], contour[i][0], contour[i][1])
            if dir1 != dir2:
                contour_simplifie.append((contour[i]))
            i += 1
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



A = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# print(simplify(solve_outlines(A)))
