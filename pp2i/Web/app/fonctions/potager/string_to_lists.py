import sys
sys.setrecursionlimit(20000)
def string_to_lists(char):
    def f2(char, liste):
        if char == '':
            return '', liste

        if char[0] == ']':
            return char[1::], liste
        if char[0] == '[':
            char, liste2 = f2(char[1::], [])
            liste.append(liste2)
            return f2(char, liste)

        if char[0] == ',' or char[0] == ' ':
            return f2(char[1::], liste)

        if char[0] == '(':
            char, liste2 = f2(char[1::], [])
            liste.append(tuple(liste2))
            return f2(char, liste)
        if char[0] == ')':
            return char[1::], liste

        nombre = ''
        while char[0] in '0123456789':
            nombre += char[0]
            char = char[1::]
        liste.append(int(nombre))
        return f2(char, liste)

    char, liste = f2(char, [])
    return liste[0]


if __name__ == "__main__":
    from time import time
    import random as rd
    import matplotlib.pyplot as plt


    def sous_listes(longueur, profondeur, liste1):
        liste = liste1.copy()
        if profondeur == 0:
            return 5, 7
        for k in range(longueur):
            ajout = sous_listes(longueur, profondeur - 1, [])
            liste.append(ajout)
        return liste

    def test(x):
        resultat = []
        for j in range(2, x):
            test = str(sous_listes(4*j, 1, []))
            t = time()
            string_to_lists(test)
            resultat.append(time() - t)
        return resultat
    resultat = []
    a = 80
    b = 5000
    res = test(a)
    temps = time()
    for k in res:
        resultat.append([k])

    for k in range(b-1):
        res = test(a)
        for i in range(len(res)):
            resultat[i].append(res[i])
    finale = []
    for i in range(len(resultat)):
        liste = sorted(resultat[i])
        finale.append(liste[len(liste)//2])
    print(time()-temps)
    plt.plot([4*k for k in range(2, a)], finale)
    plt.xlabel("Longueur de la liste testée")
    plt.ylabel("Temps (s)")
    plt.title("Médiane de chacune des valeurs sur " + str(b) + " tests")
    plt.show()
