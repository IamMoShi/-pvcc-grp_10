from PIL import Image, ImageDraw

"""
Fonctionne avec matrice de terrain
"""


def creation_image(l_polygones, tableau_potager, alpha, items, file, id_image):
    # Création de l'esquisse que l'on va peindre par la suite
    size = (len(tableau_potager[0]) * alpha, len(tableau_potager) * alpha)
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img, mode='RGB')

    for polygone in l_polygones:
        id_plante = tableau_potager[(polygone[0][1] // alpha, polygone[0][0] // alpha)]

        if id_plante == 0:
            draw.polygon(polygone, fill='#cccccc', width=1, outline=None)
        else:
            items.execute('select color from plante where id_plante = ?', (int(id_plante),))
            color = items.fetchall()[0][0]
            print(color)
            draw.polygon(polygone, fill=color, width=1, outline=None)

    img.save('app/' + file + str(id_image) + '.png', "PNG")
