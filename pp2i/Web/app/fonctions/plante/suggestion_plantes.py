import sqlite3
import random
from math import sqrt

# IMPORTANT : penser à masque la ligne suivante quand on utilise le code via l'app web (possible conflit)
#database = sqlite3.connect("app/database/database.db")

def id_to_nom(id:int,database) -> str:
# renvoie le nom d'une plante à partir de son id
    cur = database.cursor()
    cur.execute("select nom from plante where id_plante like ?",(id,))
    donnees=cur.fetchall()
    return donnees[0][0]

def liste_id_to_nom(liste_id:list,database) -> list:
# renvoie une liste de noms à partir d'une liste d'id
    liste_nom=[]
    for i in liste_id:
        liste_nom.append(id_to_nom(i,database))
    return liste_nom

def coords_to_id(x:int,y:int,liste_coords_plantes:list,liste_id_plantes:list,database) -> int:
# renvoie l'id d'une plante à partir de ses coordonnées, d'une liste des coordonnées des plantes et d'une liste des id des plantes
    for i in range(len(liste_coords_plantes)):
        if liste_coords_plantes[i]==(x,y):
            return liste_id_plantes[i]

def liste_coords_to_id(liste_coords_recherchees:list,liste_coords_plantes:list,liste_id_plantes:list,database) -> list:
# renvoie une liste d'id correspondant à la liste de coordonnées analysées
    liste_id=[]
    for i in liste_coords_recherchees:
        liste_id.append(coords_to_id(i[0],i[1],liste_coords_plantes,liste_id_plantes,database))
    return liste_id

def coords_voisins(x:int,y:int,taille:tuple,liste_coords_plantes:list,liste_tailles_plantes:list,rayon:int,database) -> list: 
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

def distances_voisins(x:int,y:int,taille:tuple,liste_coords_plantes:list,rayon:int,id_parcelle:int,liste_tailles_plantes:list,database) -> list:
# renvoie les distances des plantes dans un rayon de rayon autour des coordonnées (x,y)
    distances=[]
    voisinnage=coords_voisins(x,y,taille,liste_coords_plantes,liste_tailles_plantes,rayon,database)
    for i in voisinnage:
        x_tmp=i[0]
        y_tmp=i[1]
        delta_x=x-x_tmp
        delta_y=y-y_tmp
        if abs(delta_x)>taille[0] and abs(delta_y)>taille[1]: # si la distance est inférieure à la taille on ne peut pas planter de plante
            distances.append((delta_x, delta_y, x_tmp,y_tmp)) # valeurs d'index 0 et 1 positives si la plante est à droite / en bas
    return distances

def est_voisin(x:int,y:int,liste_coords_plantes:list,liste_tailles_plantes:list,rayon:int,database) -> bool:
# renvoie True si les coordonnées sont dans un certain rayon autour d'une plante
    for i in range(len(liste_coords_plantes)): # on teste pour toute la liste de plantes
        x_tmp=liste_coords_plantes[i][0]+liste_tailles_plantes[i]/2 # on se place au milieu de la plante
        y_tmp=liste_coords_plantes[i][1]+liste_tailles_plantes[i]/2
        if (x_tmp-x)**2+(y_tmp-y)**2<=rayon**2: # si la distance est inférieure au rayon
            return True #  on renvoie True
    return False



def plantes_compagnes(id_plante:int,database) -> list:
# renvoie les plantes compagnes d'une plante
    cur = database.cursor()
    cur.execute("select plante2 from compagnons where plante1 like ?",(id_plante,)) # on cherche les compagnons de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from compagnons where plante2 like ?",(id_plante,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def plantes_ennemies(id_plante:int,database) -> list:
# renvoie la liste des ennemis d'une plante
    cur = database.cursor()
    cur.execute("select plante2 from ennemis where plante1 like ?",(id_plante,)) # on cherche les ennemis de la plante
    donnees=cur.fetchall()
    cur.execute("select plante1 from ennemis where plante2 like ?",(id_plante,)) # on cherche dans les 2 sens (id supérieur et id inférieur)
    donnees+=cur.fetchall() # on concatène les 2 listes
    retour=[]
    for i in donnees:
        retour.append(i[0])
    return retour

def suggestion(liste_id_plantes:list,database) -> tuple:
# renvoie les id des plantes compagnes et ennemies d'une liste de plantes
    compagnes=[]
    ennemies=[]
    for i in liste_id_plantes: # on cherche les compagnes et ennemies de chaque plante
        compagnes_temp=plantes_compagnes(i,database) # liste des compagnes de la plante étudiée
        for j in compagnes_temp:
            if j not in compagnes: # on vérifie que la plante n'est pas déjà dans la liste
                compagnes.append(j) # on ajoute la plante à la liste
        ennemies_temp=plantes_ennemies(i,database) # liste des ennemis de la plante étudiée
        for j in ennemies_temp:
            if j not in ennemies: # on vérifie que la plante n'est pas déjà dans la liste
                ennemies.append(j) # on ajoute la plante à la liste
    for ennemi in ennemies:
        if ennemi in compagnes: # on vérifie que la plante n'est pas à la fois ennemie et compagne
            compagnes.remove(ennemi) # on l'enlève de la liste des compagnes si elle est aussi ennemie
# la liste compagnes contient les id des plantes compagnes et non ennemies
# la liste ennemies contient les id des plantes ennemies
    return(compagnes,ennemies)      

def aleatoire(id_parcelle:int,nombre:int,database):
# ajoute une plante aléatoire à la parcelle à une position aléatoire
    def secondaire(id_parcelle:int,database):
        cur = database.cursor()
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
            database.commit()
    for i in range(nombre,database):
        secondaire(id_parcelle)

def algo_placement(id_parcelle:int,taille:int,database) -> list:
# algo de placement
    cur = database.cursor()
    cur.execute("select x_plante,y_plante from contient where id_parcelle like ?",(id_parcelle,)) # on cherche les positions des plantes    
    donnees=cur.fetchall()
    pos_plantes=donnees.copy() # liste des positions des plantes (des milieux)
    plantes = []
    for i in range(len(pos_plantes)):
        plantes.append((pos_plantes[i])+(300,))
    return (trouve_positions(plantes, taille, id_parcelle,database))


def trouve_positions(plantes:list, taille:tuple, id_parcelle:int,database):
# sous algo de l'algo de placement (recherche les positions)

    bug=plantes.copy() #on travaille sur une copie car sinon on crée des erreurs en modifiant la liste originale
    liste_tailles_plantes=[]

    cur=database.cursor()
    cur.execute("select longueur_parcelle,largeur_parcelle from parcelle where id_parcelle like ?",(id_parcelle,))
    donnees=cur.fetchall()
    longueur_parcelle=donnees[0][0]
    largeur_parcelle=donnees[0][1]

    tmp=plantes.copy()
    for i in range(len(tmp)): # on cherche la taille de chaque plante
        cur=database.cursor()
        cur.execute("""select taille from contient as ct join plante as pl on ct.id_plante=pl.id_plante
        where id_parcelle like ? and x_plante like ? and y_plante like ?
        """,(id_parcelle,plantes[i][0],plantes[i][1]))
        donnees=cur.fetchall()
        liste_tailles_plantes.append(donnees[0][0])
        plantes[i]=(tmp[i][0],tmp[i][1])

    emplacements=[]
    for i in range(len(plantes)): # on travaille sur la liste de plantes
        x, y, rayon = bug[i]
        for j in range(-taille[0] // 2, taille[0] // 2 + 1,taille[0]): # pour chaque plante on travaille sur les 4 coins
            for k in range(-taille[1] // 2, taille[1] // 2 + 1,taille[1]): # suite des 4 coins
                if x+j<0 or y+k<0:
                    continue
                x_tmp = x + j
                y_tmp = y + k
                dist=distances_voisins(x_tmp, y_tmp, taille, plantes,rayon,id_parcelle,liste_tailles_plantes,database)
                # dist : (dist_x, dist_y, x_voisin,y_voisin)
                for i in dist:
# ATTENTION x_emplacement et y_emplacement sont les coordonnées du coin supérieur gauche
                    x_test, y_test = (x_tmp+(i[0]//2), y_tmp+(i[1]//2))
                    if x_test<taille[0]//2 or y_test<taille[1]//2:
                        continue
                    if x_test>longueur_parcelle-taille[0]//2 or y_test>largeur_parcelle-taille[1]//2:
                        continue
                    x_emplacement, y_emplacement = (x_test-taille[0]//2, y_test-taille[1]//2)
                    emplacements.append((x_emplacement, y_emplacement))

    #on enlève les doublons
    ensemble = set(emplacements) # on transforme la liste en ensemble
    emplacements = list(ensemble) # on transforme l'ensemble en liste

    return creation_dict(emplacements, taille, id_parcelle,database)

def creation_dict(emplacements:list, taille:tuple, id_parcelle:int,database):
    mon_dict={}
    for i in emplacements:
        id_compagnons=test_position(id_parcelle,taille,(i[0]+taille[0],i[1]+taille[1]),database)
        for j in id_compagnons:
            if j in mon_dict:
                mon_dict[j].append(i)
            else:
                mon_dict[j]=[i]
    return mon_dict

def test_position(id_parcelle:int,taille:tuple,pos_testee:tuple,database):
    liste_coords_plantes=[] # liste des coordonnées des plantes de la parcelle
    liste_tailles_plantes=[] # liste des tailles des plantes de la parcelle
    liste_id_plantes=[] # liste des id des plantes de la parcelle
    cur = database.cursor()
    cur.execute("select x_plante,y_plante,id_plante from contient where id_parcelle = ?",(id_parcelle,)) # on cherche les coordonnées des plantes
    donnees=cur.fetchall()
    for i in range(len(donnees)):
        liste_coords_plantes.append((donnees[i][0],donnees[i][1]))
        liste_id_plantes.append(donnees[i][2])
        cur.execute("select taille from plante where id_plante = ?",(donnees[i][2],))
        taille_plante=cur.fetchall()
        liste_tailles_plantes.append(taille_plante[0][0])
    # fin création des listes de coordonnées et de tailles des plantes
    x=pos_testee[0]
    y=pos_testee[1]
    i=(x,y)
    voisins=coords_voisins(i[0],i[1],taille,liste_coords_plantes,liste_tailles_plantes,300,database) # on cherche les voisins de la position
    id_voisins=liste_coords_to_id(voisins,liste_coords_plantes,liste_id_plantes,database) # on récupère les id des voisins
    possibles=suggestion(id_voisins,database)
    #print("Pour la position",i,"les plantes compagnes sont",liste_id_to_nom(possibles[0],database),"et les plantes ennemies sont",liste_id_to_nom(possibles[1],database))
    return possibles[0]