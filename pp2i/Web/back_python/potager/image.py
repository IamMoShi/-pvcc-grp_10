from PIL import Image, ImageDraw
import sys
import numpy as np
from os.path import dirname

sys.path.append(dirname(__file__))
import transformation_polygone_v2 as tp


class PotagerImage:
    alpha = 50  # redimensionnement des coefficients de la matrice en px
    file = 'back_python/potager/images_potagers/'

    def __init__(self, tableau_potager, id_image, items):
        self.size = (len(tableau_potager[0]) * self.alpha, len(tableau_potager) * self.alpha)
        self.tableau_potager = tableau_potager
        self.id_image = id_image

        img = Image.new('RGB', self.size, color='white')
        draw = ImageDraw.Draw(img, mode='RGB')

        l_contours = tp.solve_outlines(tableau_potager)
        l_polynomes = tp.simplify(l_contours)
        l_polynomes = tp.reverse(l_polynomes)
        l_polynomes = tp.resize_liste(l_polynomes, self.alpha)
        self.polynomes = l_polynomes

        for polynome in l_polynomes:
            id_plante = tableau_potager[(polynome[0][1] // self.alpha, polynome[0][0] // self.alpha)]
            if id_plante == 0:
                draw.polygon(polynome, fill='grey', width=1, outline=None)
            else:
                items.execute('select color from plante where id_plante = ?', (int(id_plante),))
                color = items.fetchall()[0][0]
                draw.polygon(polynome, fill=color, width=1, outline=None)

        img.save(self.file + str(id_image) + '.png', "PNG")

    def image_path(self):
        return self.file + str(self.id_image)


