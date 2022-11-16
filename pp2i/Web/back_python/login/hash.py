import hashlib 

def hash(mdp):
    return hashlib.md5(mdp.encode()).hexdigest()
