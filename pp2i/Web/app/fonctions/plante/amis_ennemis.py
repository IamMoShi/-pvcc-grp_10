def amis_ennemis(numero, database):
    # ----------------------------------------------------------------------------------------------------------#
    """
    :param numero: numéro de la plante demandée
    :param database: database
    :return:
    l_infos_amis : correspond aux compagnons de la plante
    l_infos_ennemis : correspond aux ennemis de la plante
    dico_des_erreurs : renseigne sur la potentielle erreur qui est survenue
    int : numéro de l'erreur
    """
    # ----------------------------------------------------------------------------------------------------------#
    # -----------------------------Création du dictionnaire-----------------------------------------------------#

    dico_des_erreurs = {
        0: "aucune erreur n'a été détectée",
        1: "Une erreur concernant le numéro de la plante est survenue",
        2: "Aucune plante ne possède cet id",
        3: "La plante n'a pas d'amis",
        4: "La plante n'a pas d'ennemis"
    }

    # ----------------------------------------------------------------------------------------------------------#
    # -------------------------initialisation car peut-être vide suite à une erreur-----------------------------#

    l_infos_amis, l_infos_ennemis = [], []

    # ----------------------------------------------------------------------------------------------------------#
    # ------------------------On vérifie que le numéro rentré est valide----------------------------------------#

    try:
        int(numero)
    except:
        return dico_des_erreurs, 1

    # ----------------------------------------------------------------------------------------------------------#
    # --------------------------On récupère la database pour pvr passer des commandes---------------------------#

    #database = get_db()

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------Récupération des infos sur notre plante---------------------------------------#

    items = database.cursor()
    items.execute('select * from plante where id_plante = ?', (numero,))
    resultat = items.fetchall()

    # ----------------------------------------------------------------------------------------------------------#
    # -----------------------------Si on a pas de résultat, on lance une erreur----------------------------------#

    if not resultat:
        return l_infos_amis, l_infos_ennemis, dico_des_erreurs, 0

    # ----------------------------------------------------------------------------------------------------------#
    # -----------------------------------On enregistre les résultats--------------------------------------------#

    id_plante, taille, nom, color = resultat[0]

    # ----------------------------------------------------------------------------------------------------------#
    # -------------------------On cherche les paires d'amis contenant notre plante------------------------------#

    items = database.cursor()
    items.execute('Select * from compagnons where plante1 = ? or plante2 = ?', (id_plante, id_plante,))

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    amis = items.fetchall()

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------on récupère uniquement l'id des autres plantes--------------------------------#

    amis = [paire[0] if paire[0] != id_plante else paire[1] for paire in amis]

    # ----------------------------------------------------------------------------------------------------------#
    # --------------------------initialisation liste infos sur les amis-----------------------------------------#

    l_infos_amis = []

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    for ami in amis:
        # ----------------------------------------------------------------------------------------------------------#
        # ---------------------------pour chaque amis on cherche ses informations-----------------------------------#

        items = database.cursor()
        items.execute('Select * from plante where id_plante = ?', (ami,))

        # ----------------------------------------------------------------------------------------------------------#
        # --------------------------on enregistre les informations des amis-----------------------------------------#

        l_infos_amis.append(items.fetchall())

    # ----------------------------------------------------------------------------------------------------------#
    """

    On fait la même chose pour les ennemis (cf au commentaire fait dans la première partie)

    """
    # ----------------------------------------------------------------------------------------------------------#

    items = database.cursor()
    items.execute('Select * from ennemis where plante1 = ? or plante2 = ?', (id_plante, id_plante,))

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    ennemis = items.fetchall()

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    ennemis = [paire[0] if paire[0] != id_plante else paire[1] for paire in ennemis]

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    l_infos_ennemis = []

    # ----------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------#

    for ennemi in ennemis:
        # ----------------------------------------------------------------------------------------------------------#
        # ----------------------------------------------------------------------------------------------------------#

        items = database.cursor()
        items.execute('Select * from plante where id_plante = ?', (ennemi,))

        # ----------------------------------------------------------------------------------------------------------#
        # ----------------------------------------------------------------------------------------------------------#

        l_infos_ennemis.append(items.fetchall())

    # ----------------------------------------------------------------------------------------------------------#
    # -----------------------cas où la plante n'a pas d'amis----------------------------------------------------#

    if not l_infos_amis:
        return l_infos_amis, l_infos_ennemis, dico_des_erreurs, 3

    # ----------------------------------------------------------------------------------------------------------#
    # ------------------------cas où la plante n'a pas d'ennemis------------------------------------------------#

    if not l_infos_ennemis:
        return l_infos_amis, l_infos_ennemis, dico_des_erreurs, 4

    # ----------------------------------------------------------------------------------------------------------#
    # ---------------------------cas normal---------------------------------------------------------------------#

    return l_infos_amis, l_infos_ennemis, dico_des_erreurs, 0
