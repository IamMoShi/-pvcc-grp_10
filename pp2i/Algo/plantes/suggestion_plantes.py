import sqlite3

data = sqlite3.connect("Algo/plantes/databse.db")

def plantes_compagnes(plante):
    cur = data.cursor()
    cur.execute("select id from plantes where nom like ?",(plante,)) # on cherche l'id de la plante
    donnees=cur.fetchall()
    for i in donnees:
        id=i[0]
    cur.execute("select plante2 from compagnons where plante1 like ?",(id,)) # on cherche les compagnons de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from compagnons where plante2 like ?",(id,))
    donnees+=cur.fetchall()
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def plantes_ennemies(plante):
    cur = data.cursor()
    cur.execute("select id from plantes where nom like ?",(plante,)) # on cherche l'id de la plante
    donnees=cur.fetchall()
    for i in donnees:
        id=i[0]
    cur.execute("select plante2 from ennemis where plante1 like ?",(id,)) # on cherche les ennemis de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from ennemis where plante2 like ?",(id,))
    donnees+=cur.fetchall()
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def id_to_nom(id):
    cur = data.cursor()
    cur.execute("select nom from plantes where id like ?",(id,))
    donnees=cur.fetchall()
    return donnees[0][0]

def liste_id_to_nom(liste_id:list):
    liste_nom=[]
    for i in liste_id:
        liste_nom.append(id_to_nom(i))
    return liste_nom

def suggestion(liste_plantes:list):
    compagnes=[]
    ennemies=[]
    for i in liste_plantes:
        compagnes_temp=plantes_compagnes(i)
        for j in compagnes_temp:
            if j not in compagnes:
                compagnes.append(j)
        ennemies_temp=plantes_ennemies(i)
        for j in ennemies_temp:
            if j not in ennemies:
                ennemies.append(j)
    for ennemi in ennemies:
        if ennemi in compagnes:
            print("La plante",id_to_nom(ennemi),"est à la fois ennemie et compagne")
            compagnes.remove(ennemi)
    print("Les plantes compagnes sont :",liste_id_to_nom(compagnes))
    print("Les plantes ennemies sont :",liste_id_to_nom(ennemies))        

print(liste_id_to_nom(plantes_compagnes("absinthe")))
print(liste_id_to_nom(plantes_ennemies("absinthe")))
suggestion(["absinthe","ail","aneth","anis"])
