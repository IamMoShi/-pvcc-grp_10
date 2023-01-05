from PIL import Image, ImageDraw

"""
Fonctionne avec id déjà donnés
"""


def creation_image_by_id(l_polygones, l_id, size, items, file, id_image):
    # Création de l'esquisse que l'on va peindre par la suite
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img, mode='RGB')
    i = 0
    for polygone in l_polygones:
        id_plante = l_id[i]
        i += 1

        if id_plante == 0:
            draw.polygon(polygone, fill='#cccccc', width=1, outline=None)
        else:
            items.execute('select color from plante where id_plante = ?', (int(id_plante),))
            color = items.fetchall()[0][0]
            draw.polygon(polygone, fill=color, width=1, outline=None)
    img.save(file + str(id_image) + '.png', "PNG")
    return None
