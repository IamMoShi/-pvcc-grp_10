def reverse(l_polygones):
    """
    Rotation de 90 degrés (si longueur/largeur inversée)
    """
    l_liste = []
    for polygone in l_polygones:
        liste = []
        for couple in polygone:
            liste.append((couple[1], couple[0]))
        l_liste.append(liste)
    return l_liste