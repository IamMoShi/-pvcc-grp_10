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
