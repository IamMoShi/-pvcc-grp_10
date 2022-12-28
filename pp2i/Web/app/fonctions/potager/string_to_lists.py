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
