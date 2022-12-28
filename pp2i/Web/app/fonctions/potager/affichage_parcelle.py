from .creation_image_by_id import creation_image_by_id


def affichage_parcelle(id_parcelle, id_jardin, longueur, largeur, l_polygone, l_id, items,
                       id_user=None, file='static/images/images_potagers/'):
    print('hello')
    creation_image_by_id(l_polygone, l_id, (longueur, largeur), items, file, id_parcelle)
    return file + str(id_parcelle) + '.png'
