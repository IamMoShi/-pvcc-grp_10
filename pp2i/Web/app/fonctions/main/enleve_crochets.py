def enleve_crochets(liste):
    tmp = []
    if len(liste) != 0:
        for i in range(len(liste)):
            tmp.append(liste[i][0])
    return tmp
