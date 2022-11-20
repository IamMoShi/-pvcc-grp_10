from PIL import Image, ImageDraw
import transformation_polygone as tp
import numpy as np


class PotagerImage:
    alpha = 50  # redimensionnement des coefficients de la matrice en px
    color = 'green'
    file = ''

    def __init__(self, tableau_potager, id_image):
        self.size = (len(tableau_potager) * self.alpha, len(tableau_potager[0]) * self.alpha)
        img = Image.new('RGB', self.size, color='white')
        draw = ImageDraw.Draw(img, mode='RGB')
        l_contours = tp.solve_outlines(tableau_potager)
        l_polynomes = tp.simplify(l_contours)
        l_polynomes = tp.resize_liste(l_polynomes, self.alpha)
        for polynome in l_polynomes:
            draw.polygon(polynome, fill=self.color, width=1, outline='grey')
        img.save(self.file + str(id_image) + '.jpg', "JPEG")


A = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
test = PotagerImage(A, 10)
