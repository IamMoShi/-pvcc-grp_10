def amis_ennemies(id_plante, l_paire_compagnons):
    l_amis_ennemies = []
    for paire in l_paire_compagnons:
        if paire[0] == id_plante:
            l_amis_ennemies.append(paire[1])
        else:
            l_amis_ennemies.append(paire[0])
    return l_amis_ennemies


def amis_ennemies_bis(id_plante, l_paire_compagnons):
    return [paire[0] if paire[0] != id_plante else paire[1] for paire in l_paire_compagnons]


if __name__ == "__main__":
    id_plante = 1
    l_paires = [(1, 0), (1, 10), (2, 1)]
    resultat = amis_ennemies_bis(id_plante, l_paires)
    print(resultat)
