import sqlite3
import random

data = sqlite3.connect("app/database/database.db")

def id_to_nom(id:int) -> str:
# renvoie le nom d'une plante à partir de son id
    cur = data.cursor()
    cur.execute("select nom from plante where id_plante like ?",(id,))
    donnees=cur.fetchall()
    return donnees[0][0]

def liste_id_to_nom(liste_id:list) -> list:
# renvoie une liste de noms à partir d'une liste d'id
    liste_nom=[]
    for i in liste_id:
        liste_nom.append(id_to_nom(i))
    return liste_nom

def coords_to_id(x:int,y:int,liste_coords_plantes:list,liste_id_plantes:list) -> int:
# renvoie l'id d'une plante à partir de ses coordonnées, d'une liste des coordonnées des plantes et d'une liste des id des plantes
    for i in range(len(liste_coords_plantes)):
        if liste_coords_plantes[i]==(x,y):
            return liste_id_plantes[i]

def liste_coords_to_id(liste_coords_recherchees:list,liste_coords_plantes:list,liste_id_plantes:list) -> list:
# renvoie une liste d'id correspondant à la liste de coordonnées analysées
    liste_id=[]
    for i in liste_coords_recherchees:
        liste_id.append(coords_to_id(i[0],i[1],liste_coords_plantes,liste_id_plantes))
    return liste_id

def coords_voisins(x:int,y:int,taille:int,liste_coords_plantes:list,liste_tailles_plantes:list,rayon:int) -> list: 
# renvoie les plantes dans un rayon de rayon autour des coordonnées (x,y)
    voisinnage=[]
    x+=taille/2 # pour se placer au milieu de la plante
    y+=taille/2
    for i in range(len(liste_coords_plantes)): # on teste pour toute la liste de plantes
        x_tmp=liste_coords_plantes[i][0]+liste_tailles_plantes[i]/2 # on se place au milieu de la plante
        y_tmp=liste_coords_plantes[i][1]+liste_tailles_plantes[i]/2
        if (x_tmp-x)**2+(y_tmp-y)**2<=rayon**2: # si la distance entre les deux plantes est inférieure au rayon
            voisinnage.append(liste_coords_plantes[i]) #  on ajoute la plante à la liste des plantes voisines
    return voisinnage




def plantes_compagnes(plante:int) -> list:
# renvoie les plantes compagnes d'une plante
    cur = data.cursor()
    cur.execute("select id_plante from plante where nom like ?",(plante,)) # on cherche l'id de la plante
    donnees=cur.fetchall()
    for i in donnees:
        id=i[0]
    cur.execute("select plante2 from compagnons where plante1 like ?",(id,)) # on cherche les compagnons de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from compagnons where plante2 like ?",(id,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def plantes_ennemies(plante:int) -> list:
# renvoie la liste des ennemis d'une plante
    cur = data.cursor()
    cur.execute("select id_plante from plante where nom like ?",(plante,)) # on cherche l'id de la plante
    donnees=cur.fetchall()
    for i in donnees:
        id=i[0]
    cur.execute("select plante2 from ennemis where plante1 like ?",(id,)) # on cherche les ennemis de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from ennemis where plante2 like ?",(id,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def suggestion(liste_plantes:list) -> tuple:
# renvoie les plantes compagnes et ennemies d'une liste de plantes
    compagnes=[]
    ennemies=[]
    for i in liste_plantes: # on cherche les compagnes et ennemies de chaque plante
        compagnes_temp=plantes_compagnes(i) # liste des compagnes de la plante étudiée
        for j in compagnes_temp:
            if j not in compagnes: # on vérifie que la plante n'est pas déjà dans la liste
                compagnes.append(j) # on ajoute la plante à la liste
        ennemies_temp=plantes_ennemies(i) # liste des ennemis de la plante étudiée
        for j in ennemies_temp:
            if j not in ennemies: # on vérifie que la plante n'est pas déjà dans la liste
                ennemies.append(j) # on ajoute la plante à la liste
    for ennemi in ennemies:
        if ennemi in compagnes: # on vérifie que la plante n'est pas à la fois ennemie et compagne
            print("La plante",id_to_nom(ennemi),"est à la fois ennemie et compagne")
            compagnes.remove(ennemi) # on l'enlève de la liste des compagnes si elle est aussi ennemie
# la liste compagnes contient les id des plantes compagnes et non ennemies
# la liste ennemies contient les id des plantes ennemies
    return(compagnes,ennemies)      


def aleatoire(id_parcelle:int):
# ajoute une plante aléatoire à la parcelle à une position aléatoire
    cur = data.cursor()
    cur.execute("select max(id_plante) from plante") # on cherche l'id maximum des plantes
    donnees=cur.fetchall()
    max_id=donnees[0][0]
    id=random.randint(1,max_id) # on choisit une plante aléatoire
    x=random.randint(0,100)
    y=random.randint(0,100)
    cur.execute("select * from contient where x_plante = ? and y_plante = ?",(x,y)) # on vérifie que la position est libre
    if cur.fetchall()==[]: # si la position est libre
        cur.execute("insert into contient values(?,?,?,?)",(id_parcelle,id,x,y)) # on ajoute la plante à la parcelle
        data.commit()

def positions_libres(id_parcelle:int,taille:tuple) -> list:
# renvoie les positions libres d'une certaine taille d'une parcelle
# taille correspond à la hauteur et à la largeur de l'espace libre que l'on cherche
    cur = data.cursor()
    cur.execute("select x_plante,y_plante,id_plante from contient where id_parcelle = ?",(id_parcelle,)) # on cherche les positions occupées
    donnees=cur.fetchall()
    tailles = [] # liste des tailles des plantes
    for i in range(len(donnees)):
        cur.execute("select taille from plante where id_plante = ?",(donnees[i][2],))
        taille_plante=cur.fetchall()
        tailles.append(taille_plante[0][0])
        donnees[i]=(donnees[i][0],donnees[i][1]) # on ne garde que les coordonnées
    positions_occupées=donnees.copy()
    for i in range(len(donnees)):
        for j in range(0,tailles[i]+1):
            for k in range(0,tailles[i]+1):
                positions_occupées.append((donnees[i][0]+j,donnees[i][1]+k)) # on ajoute chaque position occupée par les plantes (chaque unique couple de coordonnées)

    # on récupère les dimensions de la parcelle
    cur.execute("select longueur_parcelle,largeur_parcelle from parcelle where id_parcelle = ?",(id_parcelle,))
    dimensions=cur.fetchall()[0]
    x_parcelle=int(dimensions[0])
    y_parcelle=int(dimensions[1])

    positions_libres = []
    for i in range(0,x_parcelle-taille[0]): # on parcourt la parcelle
        for j in range(0,y_parcelle-taille[1]):
            if (i,j) not in positions_occupées and (i+taille[0],j+taille[1]) not in positions_occupées and (i+taille[0],j) not in positions_occupées and (i,j+taille[1]) not in positions_occupées:
# on vérifie que les 4 coins de l'espace voulu sont libres (donc que l'espace de la taille voulue est libre)
                positions_libres.append((i,j))
    return positions_libres

positions_libres(2,(20,20))