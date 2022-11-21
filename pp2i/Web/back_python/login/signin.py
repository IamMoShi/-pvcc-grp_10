import re

def signin(email, password):
    b_email, b_password = False, False

    min_cara, max_cara = 8, 16
    str_cara = "@$!%*?&_-"
    msg = ''


    r_email = "^[a-zA-Z0-9._-]+[@]{1}[a-zA-Z0-9._-]+[.]{1}[a-z]{2,10}$"
    if re.search(r_email, email):
        b_email = True
    else:
        msg = msg + 'Email invalide ; '



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

    if b_email and b_password:
        return True
    return False



    