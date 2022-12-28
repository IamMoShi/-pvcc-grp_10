def to_text(l_polygones, l_id_plante):
    l_polygones_txt = []
    longueur = len(l_polygones)

    for k in range(longueur):
        polygone_txt = ""
        polygone = l_polygones[k]
        for couple in polygone:
            polygone_txt += str(couple[0]) + ',' + str(couple[1]) + ','
        id_plante = l_id_plante[k]
        l_polygones_txt.append((polygone_txt, id_plante))
    return l_polygones_txt