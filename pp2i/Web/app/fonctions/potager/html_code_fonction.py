from .transformation_polygone_v2 import *


def html_code_fonction(l_polygones, l_id, id_image=0, file=''):
    """
    :return: (list[str], str), change le formatage de l'information contenue dans l_polygone pour facilité
    la lecture dans le fichier html
    Donne l'endroit où se trouve l'image correspondante à l'objet
    """
    l_polygones_txt = to_text(l_polygones, l_id)
    chemin_image = "/" + file + str(id_image) + '.png'
    return l_polygones_txt, chemin_image
