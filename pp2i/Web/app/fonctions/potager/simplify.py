from transformation_polygone_v2 import give_direction


def simplify(l_contours):
    l_contours_simplifie = []

    for contour in l_contours:
        contour_simplifie = [contour[0]]
        len_contour = len(contour)
        direction = 1

        for k in range(1, len_contour):
            a, b = contour[k - 1]
            x, y = contour[k]
            if direction != give_direction(a, b, x, y):
                contour_simplifie.append(contour[k - 1])
                direction = give_direction(a, b, x, y)

        l_contours_simplifie.append(contour_simplifie)
    return l_contours_simplifie
