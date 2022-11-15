import numpy as np


def pair(poly):
    long = len(poly)
    poly_copy = poly.copy()
    l_pair = []
    for k in range(long // 2):
        l_pair.append(poly_copy[:2])
        poly_copy = poly_copy[2::]
    return l_pair


def previous(a, b, direction):
    if direction == (1, 0):
        return [a - 1, b]
    if direction == (-1, 0):
        return [a + 1, b]
    if direction == (0, 1):
        return [a, b - 1]
    if direction == (0, -1):
        return [a, b + 1]


def next_elt(a1, b1, direction, longueur, largeur):
    if direction == (1, 0):
        if a1 + 1 < longueur:
            return True, a1 + 1, b1
        return False, a1, b1
    if direction == (-1, 0):
        if a1 - 1 >= 0:
            return True, a1 - 1, b1
        return False, a1, b1
    if direction == (0, 1):
        if b1 + 1 < largeur:
            return True, a1, b1 + 1
        return False, a1, b1
    if direction == (0, -1):
        if b1 - 1 >= 0:
            return True, a1, b1 - 1
        return False, a1, b1
    return False, a1, b1


def sides(a, b, longueur, largeur):
    cotes = []
    if a + 1 < longueur:
        cotes.append([a + 1, b])
    if a - 1 >= 0:
        cotes.append([a - 1, b])
    if b + 1 < largeur:
        cotes.append([a, b + 1])
    if b - 1 >= 0:
        cotes.append([a, b - 1])
    return cotes


def test_sides(a1, b1, tableau_potager, longueur, largeur):
    id_plante = tableau_potager[a1, b1]
    cotes = sides(a1, b1, longueur, largeur)
    same, diff = 0, 0
    for k in cotes:
        if np.array_equal(id_plante, tableau_potager[k[0], k[1]]):
            same += 1
        else:
            diff += 0

    if same == 2:
        return False

    if same == 4:
        return False
    if a1 == 1 and b1 == 4:
        print(same)
    return True


def line(a, b, tableau_potager, direction, longueur, largeur):
    if direction == (1, 0):
        a += 1
        while a < longueur:
            if test_sides(a, b, tableau_potager, longueur, largeur):
                a += 1
            else:
                return [a, b]
        a += -1
    if direction == (-1, 0):
        a += -1
        while a >= 0:
            if test_sides(a, b, tableau_potager, longueur, largeur):
                a -= 1
            else:
                return [a, b]
        a += 1
    if direction == (0, 1):
        b += 1
        while b < largeur:
            if test_sides(a, b, tableau_potager, longueur, largeur):
                b += 1
            else:
                return [a, b]
        b += -1
    if direction == (0, -1):
        b -= 1
        while b >= 0:
            if test_sides(a, b, tableau_potager, longueur, largeur):
                b -= 1
            else:
                return [a, b]
        b += 1
    return [a, b]


def turn(a1, b1, tableau_potager, direction, longueur, largeur):
    cotes = sides(a1, b1, longueur, largeur)
    a0, b0 = previous(a1, b1, direction)
    a2, b2 = next_elt(a1, b1, direction, longueur, largeur)[1::]
    id_plante = tableau_potager[a1, b1]

    while [a0, b0] in cotes:
        cotes.remove([a0, b0])

    while [a2, b2] in cotes:
        cotes.remove([a2, b2])

    if a1 == 2 and b1 == 1:
        print(cotes)

    bon_cotes = []
    for k in cotes:
        if tableau_potager[k[0], k[1]] == id_plante:
            bon_cotes.append(k)

    if len(bon_cotes) == 1:
        return bon_cotes[0]
    if a1 == 1 and b1 == 4:
        print(cotes, test_sides(2, 4, tableau_potager, longueur, largeur))

    for k in cotes:
        if test_sides(k[0], k[1], tableau_potager, longueur, largeur):
            return k
    return 'bite'


def polynomial_searcher(i, j, tableau_potager, longueur, largeur):
    poly = [i, j]
    a = i + 1
    b = j
    direction = (1, 0)
    while a != i or b != j:
        ligne = line(a, b, tableau_potager, direction, longueur, largeur)
        a, b = ligne[0], ligne[1]
        poly.extend(ligne)
        tourne = turn(a, b, tableau_potager, direction, longueur, largeur)
        print('tourne : ' + str(tourne) + ' poly : ' + str(poly) + ' a,b : ' + str(a) + ',' + str(b))
        a2, b2 = tourne[0], tourne[1]
        direction = (a2 - a, b2 - b)
    return poly


def affichage(poly):
    long = len(poly)
    for i in range(long // 2):
        print(poly[:2])
        poly = poly[2::]
    return None


A = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1]
])
affichage(polynomial_searcher(0, 0, A, 4, 5))
