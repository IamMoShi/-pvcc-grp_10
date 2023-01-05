def legende_fonction(items, l_id):
    """
    :param: items : cursor de la database
    :return: la liste des couleurs et des noms associées à chaque plante présente dans le jardin
    """
    l_legende = [('grey', 0)]
    l_id_uniq = []

    for id in l_id:
        items.execute('select color from plante where id_plante = ?', (int(id),))
        result = items.fetchall()
        if len(result) == 1 and id not in l_id_uniq:
            l_id_uniq.append(id)
            l_legende.append((result[0][0], id))
    return l_legende