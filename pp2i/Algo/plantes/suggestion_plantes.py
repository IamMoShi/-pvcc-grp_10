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

def coords_voisins(x:int,y:int,taille:tuple,liste_coords_plantes:list,liste_tailles_plantes:list,rayon:int) -> list: 
# renvoie les plantes dans un rayon de rayon autour des coordonnées (x,y)
    voisinnage=[]
    x+=taille[0]/2 # pour se placer au milieu de la plante
    y+=taille[1]/2
    for i in range(len(liste_coords_plantes)): # on teste pour toute la liste de plantes
        x_tmp=liste_coords_plantes[i][0]+liste_tailles_plantes[i]/2 # on se place au milieu de la plante
        y_tmp=liste_coords_plantes[i][1]+liste_tailles_plantes[i]/2
        if (x_tmp-x)**2+(y_tmp-y)**2<=rayon**2: # si la distance entre les deux plantes est inférieure au rayon
            voisinnage.append(liste_coords_plantes[i]) #  on ajoute la plante à la liste des plantes voisines
    return voisinnage

def est_voisin(x:int,y:int,liste_coords_plantes:list,liste_tailles_plantes:list,rayon:int) -> bool:
# renvoie True si les coordonnées sont dans un certain rayon autour d'une plante
    for i in range(len(liste_coords_plantes)): # on teste pour toute la liste de plantes
        x_tmp=liste_coords_plantes[i][0]+liste_tailles_plantes[i]/2 # on se place au milieu de la plante
        y_tmp=liste_coords_plantes[i][1]+liste_tailles_plantes[i]/2
        if (x_tmp-x)**2+(y_tmp-y)**2<=rayon**2: # si la distance est inférieure au rayon
            return True #  on renvoie True
    return False



def plantes_compagnes(id_plante:int) -> list:
# renvoie les plantes compagnes d'une plante
    cur = data.cursor()
    cur.execute("select plante2 from compagnons where plante1 like ?",(id_plante,)) # on cherche les compagnons de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from compagnons where plante2 like ?",(id_plante,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def plantes_ennemies(id_plante:int) -> list:
# renvoie la liste des ennemis d'une plante
    cur = data.cursor()
    cur.execute("select plante2 from ennemis where plante1 like ?",(id_plante,)) # on cherche les ennemis de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from ennemis where plante2 like ?",(id_plante,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def suggestion(liste_id_plantes:list) -> tuple:
# renvoie les id des plantes compagnes et ennemies d'une liste de plantes
    compagnes=[]
    ennemies=[]
    for i in liste_id_plantes: # on cherche les compagnes et ennemies de chaque plante
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
            compagnes.remove(ennemi) # on l'enlève de la liste des compagnes si elle est aussi ennemie
# la liste compagnes contient les id des plantes compagnes et non ennemies
# la liste ennemies contient les id des plantes ennemies
    return(compagnes,ennemies)      


def aleatoire(id_parcelle:int,nombre:int):
# ajoute une plante aléatoire à la parcelle à une position aléatoire
    def secondaire(id_parcelle:int):
        cur = data.cursor()
        cur.execute("select max(id_plante) from plante") # on cherche l'id maximum des plantes
        donnees=cur.fetchall()
        max_id=donnees[0][0]
        id=random.randint(1,max_id) # on choisit une plante aléatoire
        cur.execute("select longueur_parcelle,largeur_parcelle from parcelle where id_parcelle like ?",(id_parcelle,)) # on cherche la taille de la parcelle
        donnees2=cur.fetchall()
        x=random.randint(0,donnees2[0][0])
        y=random.randint(0,donnees2[0][1])
        cur.execute("select * from contient where x_plante = ? and y_plante = ?",(x,y)) # on vérifie que la position est libre
        if cur.fetchall()==[]: # si la position est libre
            cur.execute("insert into contient values(?,?,?,?)",(id_parcelle,id,x,y)) # on ajoute la plante à la parcelle
            data.commit()
    for i in range(nombre):
        secondaire(id_parcelle)

def positions_libres(id_parcelle:int,taille:int) -> list:
# renvoie les positions sans influence d'autres plantes et les positions sous influence d'autres plantes
    cur = data.cursor()
    cur.execute("select x_plante,y_plante from contient where id_parcelle like ?",(id_parcelle,)) # on cherche les positions des plantes    
    donnees=cur.fetchall()
    pos_plantes=donnees.copy() # liste des positions des plantes (des milieux)
    pos_occupees_plantes=donnees.copy() # liste de ttes les positions occupées par chaque plante
    tmp=donnees.copy()
    liste_tailles=[]
    for i in tmp:
        cur.execute("select taille from contient join plante on contient.id_plante=plante.id_plante where x_plante like ? and y_plante like ?",(i[0],i[1])) # on cherche la taille de la plante
        donnees2=cur.fetchall()[0][0]
        liste_tailles.append(donnees2)
        liste=[(x, y) for x in range(int((-donnees2/2)+i[0]), int((donnees2/2)+1+i[0])) for y in range(int((-donnees2/2)+i[1]), int((donnees2/2)+1+i[1]))]
        pos_occupees_plantes+=liste


    cur.execute("select longueur_parcelle,largeur_parcelle from parcelle where id_parcelle like ?",(id_parcelle,)) # on cherche la taille de la parcelle
    dimensions=cur.fetchall()
    pos_free=[] # liste des positions sans influence d'autres plantes
    pos_influence=[] # liste des positions sous influence d'autres plantes
    tmp=[]
    x=0
    y=0
    while y<int(dimensions[0][1]):
        if tmp[0][0] and tmp[0][1]:
            tmp.pop(0)
        if not est_voisin(x,y,pos_plantes,liste_tailles,300):
            tmp.append((x,y))
            x+=19
        x+=1
        if x>=int(dimensions[0][0]):
            x=0
            y+=1
    return(pos_free,pos_influence)

def test_positions(id_parcelle:int,taille:tuple,pos_testees:list):
    liste_coords_plantes=[] # liste des coordonnées des plantes de la parcelle
    liste_tailles_plantes=[] # liste des tailles des plantes de la parcelle
    liste_id_plantes=[] # liste des id des plantes de la parcelle
    cur = data.cursor()
    cur.execute("select x_plante,y_plante,id_plante from contient where id_parcelle = ?",(id_parcelle,)) # on cherche les coordonnées des plantes
    donnees=cur.fetchall()
    for i in range(len(donnees)):
        liste_coords_plantes.append((donnees[i][0],donnees[i][1]))
        liste_id_plantes.append(donnees[i][2])
        cur.execute("select taille from plante where id_plante = ?",(donnees[i][2],))
        taille_plante=cur.fetchall()
        liste_tailles_plantes.append(taille_plante[0][0])
    # fin création des listes de coordonnées et de tailles des plantes
    for i in pos_testees:
        voisins=coords_voisins(i[0],i[1],taille,liste_coords_plantes,liste_tailles_plantes,300) # on cherche les voisins de la position
        id_voisins=liste_coords_to_id(voisins,liste_coords_plantes,liste_id_plantes) # on récupère les id des voisins
        possibles=suggestion(id_voisins)
        print("Pour la position",i,"les plantes compagnes sont",liste_id_to_nom(possibles[0]),"et les plantes ennemies sont",liste_id_to_nom(possibles[1]))

print(positions_libres(29,(20,20)))