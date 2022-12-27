import sqlite3
import re
from PyPDF2 import PdfReader
import random

""" Lecture du document """
reader = PdfReader("plantes/compagnonnage.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"


""" Gestion des erreurs de lecture """
text=text.replace("Le compagnonnage","")
text=text.replace("Bruxelles","bruxelles") # mot avec majuscule --> indésirable dans la DB
text=text.replace("fraise","fraisier") # nom similaire pour 2 plantes --> remplacer
text=text.replace("concombre et cornichon","concombre") # remplacement car le concombre est sans cesse associé au cornichon qui est une sous-espèce de concombre
text=text.replace("Concombre et cornichon","Concombre")
text=text.replace("Aubergin e","Aubergine ") # erreur unique pour cette plante (espace au milieu)
text=text.replace("Ail","Ail ")
text=text.replace(" -","-") # les tirets des noms sont précédés d'espaces
text=text.replace("É","E") # enlever les accents
text=text.replace("È","E") 
text=text.replace("é","e")
text=text.replace("è","e")
text=text.replace("à","a")
text=text.replace("À","A")
""" Fin des différents cas d'erreurs de lecture """


""" Split de la donnée en fonction des retours à la ligne """
pattern = r'\n'
d = re.split(pattern,text)



document =  []
current_line = []
for i in d:
    if re.match(r'.*(Legumes)+.*',i):
        continue
    if re.match(r'[A-Z].*',i): # début du tri des données
        document.append(current_line)
        current_line=[]
    current_line.append(i)
document.append(current_line)



for line in document: # enlever certains éléments ne contenant rien ou des espaces
    if re.match(r'(\s)+',line[0]):
        document.remove(line)
    if re.match(r'.*\s(et)\s.*',line[0]): 
        document.remove(line)


new_doc=[]
new_line=[]
for line in document:
    new_line=re.split(r'(\s\s)',line[0])
    for i in range(1,len(line)):
        new_line.append(line[i])
    for i in new_line:
        if re.match(r'(\s)+',i):
            new_line.remove(i)
    new_doc.append(new_line)
    new_line=[]
document=new_doc

for i in range(0,len(document)-1): # erreur unique avec la plante Rue
    test=document[i]
    if re.match(r'.*(Rue).*',test[0]):
        document.remove(test)


new_doc=[]
for test in document: # pour séparer compagnes et ennemies de la plante étudiée
    k=""
    
    new_line=[]
    new_line.append(test[0].lower())

    for i in range(1,len(test)): # on concatène toute la donnée à propos de la plante étudiée qui a l'index 0
        k=str(k+"  "+test[i])

    while re.match(r'.*(,)+\s+.*',k): # on colle les virgules aux mots pour ne pas avoir de faux espacements
        k=k.replace(", ",",")
    while re.match(r'.*\s+(,)+.*',k):
        k=k.replace(" ,",",")


    """ correction d'erreurs uniques"""
    const = True
    if const : 
        while re.match(r'.*\s{2,}(de)+.*',k):
            k=k.replace(" de","de")
        while re.match(r'.*(de)+\s{2,}.*',k):
            k=k.replace("de ","de")

        while re.match(r'.*(piment)+\s{2,}(fort)+.*',k):
            k=k.replace("piment ","piment")

        while re.match(r'.*(chou-)+\s+(fleur)+.*',k):
            k=k.replace(" fleur","fleur")

        while re.match(r'.*(chou)+\s+(rave)+.*',k):
            k=k.replace(" rave","rave")

        while re.match(r'.*(a)+\s{2,}(carde)+.*',k):
            k=k.replace("a ","a")
        
        while re.match(r'.*(chicoree)+\s{2,}(frisee)+.*',k):
            k=k.replace("chicoree ","chicoree")

        while re.match(r'.*(haricot)+\s{2,}(nain)+.*',k):
            k=k.replace("haricot ","haricot")

        while re.match(r'.*(tomat e)+.*',k):
            k=k.replace("tomat e","tomate ")

        while re.match(r'.*(ro quette)+.*',k):
            k=k.replace("ro quette","roquette")

        while re.match(r'.*(rue)+\s+.*',k):
            k=k.replace("rue ","rue")

        while re.match(r'.*(deterre)+.*',k):
            k=k.replace("deterre","de terre")

        while re.match(r'.*(menth)+\s+.*',k):
            k=k.replace("menth e","menthe")

        while re.match(r'.*(me)+\s+(nthe)+.*',k):
            k=k.replace("me nthe","menthe")

        while re.match(r'.*(terre)+\s+(epinard)+.*',k):
            k=k.replace("pomme de terre epinard","pomme de terre,epinard")

        while re.match(r'.*(echal)+\s+(ote)+.*',k):
            k=k.replace("echal ote","echalote")
        
        k=k.replace("chou debruxelles","chou de bruxelles")
        
        k=k.replace("ci boulette","ciboulette")

        k=k.replace("haricota ecosser","haricot a ecosser")

        k=k.replace("ha ricot","haricot")

        k=k.replace("courgett e","courgette")

        while re.match(r'.*(rueabsinthe)+.*',k):
            k=k.replace("rueabsinthe","rue  absinthe")

    """ fin correction d'erreurs uniques """


    pattern = r'\s{2}'
    d = re.split(pattern,k) # on split au niveau des espaces doubles (pattern entre les colonnes "compagnon" et "ennemi")

    while d.count('')!=0: # enlever certains éléments ne contenant rien
        d.remove('')

    """ on traite chaque liste compagnons et ennemis pour isoler en fonction des virgules """
    liste_finale=[]
    for element in d:
        if element==' ':
            liste_finale.append([])
        else:
            donnees=re.split(r',',element)
            liste_finale.append(donnees)
    d=liste_finale.copy()
    """ on obtient la donnée voulue """

    new_line.append(d[0])
    new_line.append(d[1])
    new_doc.append(new_line)

document=new_doc


data = sqlite3.connect("plantes/database.db") # ATTENTION LA DATABASE DOIT CONTENIR AU MOINS UNE PLANTE AVEC UN ID


def int_to_code_couleur_hexa(n:int):
    """ convertit un entier en code couleur hexadécimal """

    r = hex(random.randint(0, 255)).lstrip("0x").rjust(2, "0")
    g = hex(random.randint(0, 255)).lstrip("0x").rjust(2, "0")
    b = hex(random.randint(0, 255)).lstrip("0x").rjust(2, "0")

    return "#" + r + g + b

cur = data.cursor()
cur.execute("select * from plante") # on cherche si il existe déjà une plante
if cur.fetchall()==[]: # si aucune plante n'existe on en ajoute une
    cur.execute("insert into plante (id_plante,nom,taille,color) values(1,'absinthe',20,?)",(int_to_code_couleur_hexa(1),))
    data.commit()

def new_value(type,plante1,plante2=1):

    # pour les relations "compangons" et "ennemis", le premier ID est TOUJOURS le plus petit pour ne pas avoir de problèmes de doublons
    # la constraint id1<id2 permet aussi de ne pas lier le même élément à lui même

    if type=="plante": # ajout d'une plante dans la base plante
        cur = data.cursor()
        cur.execute("select id_plante from plante where nom like ?",(plante1,)) # on cherche si la plante existe déjà
        if cur.fetchall()==[]: # si la plante n'existe pas encore on l'ajoute
            max_value=cur.execute("select max(id_plante) from plante").fetchall()[0][0]
            cur.execute("insert into plante (id_plante,nom,taille,color) values(1+(select max(id_plante) from plante),?,20,?)",(plante1,int_to_code_couleur_hexa(max_value+1)))
            data.commit()


    elif type=="compagnon": #ajout d'une relation "compagnon" entre 2 plantes
        new_value("plante",plante1) # on vérifie si les 2 plantes sont dans la base de données et on les ajoute si besoin
        new_value("plante",plante2)

        """ on récupère l'ID de la plante 1 """
        cur = data.cursor()
        cur.execute("select id_plante from plante where nom like ?",(plante1,)) 
        for i in cur.fetchall():
            id1=i[0]

        """ on récupère l'ID de la plante 2 """
        cur.execute("select id_plante from plante where nom like ?",(plante2,))
        for i in cur.fetchall():
            id2=i[0]

        cur.execute("select plante1 from compagnons where plante1 like ? and plante2 like ?",(min(id1,id2),max(id1,id2))) # on vérifie que la relation n'existe pas encore
        if cur.fetchall()==[]: #si la relation n'existe pas encore, on l'ajoute
            cur.execute("""insert into compagnons values(?,?);""",(min(id1,id2),max(id1,id2)))
            data.commit()


    elif type=="ennemi": #ajout d'une relation "ennemi" entre 2 plantes
        new_value("plante",plante1) # on vérifie si les 2 plantes sont dans la base de données et on les ajoute si besoin
        new_value("plante",plante2)

        """ on récupère l'ID de la plante 1 """
        cur = data.cursor()
        cur.execute("select id_plante from plante where nom like ?",(plante1,))
        for i in cur.fetchall():
            id1=i[0]

        """ on récupère l'ID de la plante 2 """
        cur.execute("select id_plante from plante where nom like ?",(plante2,))
        for i in cur.fetchall():
            id2=i[0]

        cur.execute("select plante1 from ennemis where plante1 like ? and plante2 like ?",(min(id1,id2),max(id1,id2))) #on vérifie que la relation n'existe pas
        if cur.fetchall()==[]: # si la relation n'existe pas on l'ajoute
            cur.execute("""insert into ennemis values(?,?);""",(min(id1,id2),max(id1,id2)))
            data.commit()

""" Pour ajouter toutes les données du document """
for lignes in document:
    plante_etudiee = lignes[0]
    for i in lignes[1]:
        if i != plante_etudiee and i!= "":
            new_value("compagnon",plante_etudiee,i)
    for i in lignes[2]:
        if i != plante_etudiee and i!= "":
            new_value("ennemi",plante_etudiee,i)