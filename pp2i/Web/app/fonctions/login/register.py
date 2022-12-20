import re


def register(lastname: str, firstname: str, email: str, password: str, confirmation: str):
    """
    :param lastname : récupération de l'input lastname de la page register.html via requête POST
    :param firstname : récupération de firstname
    :param email: Etc...
    :param password:
    :param confirmation:
    :return : retourne une liste [boolean, ListeB: list, msg: str]
    Boolean : True si toutes les conditions sont remplies, False sinon
    ListeB : liste de booléen sur la validité des infos fournies via le POST
    msg : Renvoie un message récapitulant les erreurs présentes dans les données d'entrée
    """

    """
    Définition d'une série de booléens validant chacun des paramètres (b_nom_du_paramètre)
    """
    b_lastname, b_firstname, b_email = False, False, False
    b_password, b_confirmation = False, False
    min_cara, max_cara = 8, 16
    str_cara = "@$!%*?&_-"
    msg = ''

    """
    Test du lastname ; conditions de validité : 
        - commencer par une Majuscule
        - Posséder au moins une lettre
        - Ne pas comporter d'espaces ou de caractères spéciaux
    """

    if not (re.search("^[A-Z]", lastname)):
        msg = msg + 'Le nom ne commence pas par une majuscule ; '
    elif not (re.search("[A-Za-z]+", lastname)):
        msg = msg + 'Le nom ne contient pas assez de lettres ; '
    elif re.search("\W", lastname):
        msg = msg + 'Le nom contient un caractère spécial ou un chiffre'
    else:
        b_lastname = True

    """
    Test du firstname ; conditions de validité :
        - les mêmes que pour le nom
    """

    if not (re.search("^[A-Z]", firstname)):
        msg = msg + 'Le prenom ne commence pas par une majuscule ; '
    elif not (re.search("[A-Za-z]+", firstname)):
        msg = msg + 'Le prenom ne contient pas assez de lettres ; '
    elif re.search("\W", firstname):
        msg = msg + 'Le prénom contient un caractère spécial ou un chiffre'
    else:
        b_firstname = True

    """ 
    Test de l'email ; conditions de validité :
        - passer la regex suivante : ^[a-zA-Z0-9._-]+[@]{1}[a-zA-Z0-9._-]+[.]{1}[a-z]{2,10}$
    """

    r_email = "^[a-zA-Z0-9._-]+[@]{1}[a-zA-Z0-9._-]+[.]{1}[a-z]{2,10}$"
    if re.search(r_email, email):
        b_email = True
    else:
        msg = msg + 'Email invalide ; '

    """
    Test du password ; condition de validité :
        - longueur minimal de min_cara
        - longueur maximal de max_cara
        - doit contenir une majuscule
        - doit contenir une minuscule
        - doit contenir un chiffre
        - doit contenir un caractère spécial compris dans la str str_cara : str
        - ne doit pas contenir d'autres caractères spéciaux
        - le mot de passe ne doit pas contenir d'espace
    """
    if len(password) < min_cara:
        msg = msg + 'Le mot de passe fait moins de min_cara caractères ; '
    elif len(password) > max_cara:
        msg = msg + 'Le mot de passe fait plus de max_cara caractères ; '
    elif not (re.search("[A-Z]", password)):
        msg = msg + 'Le mot de passe ne contient pas de majuscules ; '
    elif not (re.search("[a-z]", password)):
        msg = msg + 'Le mot de passe ne contient pas de minuscules ; '
    elif not (re.search("[0-9]", password)):
        msg = msg + 'Le mot de passe ne contient pas de chiffres ; '
    elif not (re.search("["+str_cara+"]", password)):
        msg = msg + 'Le mot de passe ne contient pas de caractère spécial de la liste ; '
    elif re.search("\s", password):
        msg = msg + 'Le mot de passe contient un espace ; '
    elif not(re.search("^[a-zA-Z0-9"+str_cara+"]+$", password)):
        msg = msg + 'Un caractère n\'est pas correct ; '
    else:
        b_password = True

    """
    Test de la validation du mot de passe ; conditions de validité :
        - Doit être identique au mot de passe rentré
    """
    if password == confirmation:
        b_confirmation = True
    else:
        msg = msg + 'La confirmation du mot de passe n\'est pas correcte'

    if b_lastname and b_firstname and b_email and b_password and b_confirmation:
        entry_valid = True
    else:
        entry_valid = False
    return [entry_valid, [b_lastname, b_firstname, b_email, b_password, b_confirmation], msg]

'''
Petite zone de test

nom = "Fornoff"
prenom = "Léo"
email = "leo.fornoff@telecomnancy.net"
password = "Test123@"
confirmation = "Test123@"

print(register(nom, prenom, email, password, confirmation))

doit retourner [True, [True, True, True, True, True], ''] 
'''
