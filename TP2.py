""" BELALOUI SAMY ABDELMADJID - G1 """

#Afficher toutes les lettres en Majuscule
def AfficherMaj():
    base = ord("A")
        
    for i in range(26):
        print("[{}]" .format(chr(base + i)))

#Afficher toutes les lettres en Minuscule
def AfficherMin():
    base = ord("a")
        
    for i in range(26):
        print("[{}], " .format(chr(base + i)))
        
# (cette fonction verifie si une lettre est minuscule)
def verifMin(lettre):
    
    #unicode de la lettre choisie
    i = ord(lettre)
    
    #si l'unicode de la lettre utilisée est entre celui de "a" et "z", on retourne vrai
    if(i >= ord("a") and i <= ord("z")):
        return True

    #sinon faux
    return False

# (cette focntion fait passer une lettre minuscule en majuscule)
def mettreMaj(lettre):
    i = ord(lettre)
    
    # Vérifie si la lettre est alphabétique (majuscule ou minuscule)
    if not (ord("A") <= i <= ord("Z") or ord("a") <= i <= ord("z")):
        raise Exception("Lettre non alphabétique saisie.")
    
    # Si c'est une minuscule, on la passe en majuscule
    if verifMin(lettre):
        lettre = chr(i - 32)
    return lettre

def CesarLettre(lettre, k):
    i = ord(lettre)
    
    #si le caractere n'est pas alphabetique
    if not (ord("A") <= i <= ord("Z") or ord("a") <= i <= ord("z")):
        #lever exception
        raise Exception("le message doit etre uniquement composé de caractéres alphabétiques")
    
    #si la lettre est en minuscule, on la passe en majuscule
    if(verifMin(lettre)):
        lettre = mettreMaj(lettre)
        i = ord(lettre) # on prend l'ordre de la nouvelle lettre
       
        
    decalage = (i - ord("A") + k)
    lettre = chr(ord("A") + decalage % 26)  #cypher = (plain + k) mod 26

    return lettre

def CesarTexte(texte, k):
    cyphertext = ""
    try:
        #on fait un decalage a chaque lettre du message
        for lt in texte:
            lt = CesarLettre(lt, k)
            cyphertext += lt
    
    except Exception as e:
        raise Exception(e)
        
    return cyphertext

# cette fonction de dechiffrer un message avec toutes les decalages possibles (César)
def ForceBrute(cypher):
        
    #effectuer tous les dechiffrements César possibles (de 0 à 25)
    for k in range(26):
        plain = CesarTexte(cypher, -k)
        print(" K: {} : [{}]" .format(k, plain))
        
def supprime_accents_minuscules_ponctuations(message):
    resultat = ""
    e = ["é", "è", "ê", "ë"]
    a = ["à", "â"]
    u = ["ù", "û"]
    i = ["î"]
    o = ["ô"]
    c = ["ç"]
    
    #parcourir chaque lettre du message
    for lettre in message:
        
        # Refuser les chiffres
        if lettre.isdigit():
            raise Exception("Le message ne doit pas contenir de chiffres.")
        
        #si une lettre contient un accent, on le lui retire
        if(lettre in e):
            lettre = "e"
        elif(lettre in a):
            lettre = "a"
        elif(lettre in u):
            lettre = "u"
        elif(lettre in o):
            lettre = "o"
        elif(lettre in c):
            lettre = "c"
        elif(lettre in i):    
            lettre = "i"
        
        try:
        #si une lettre est en minuscule, on la rend en majuscule
            if(verifMin(lettre)):
                lettre = mettreMaj(lettre)
        except Exception as e:
            raise Exception(e)
            
        #on ajoute la lettre au resultat uniquement s'il s'agit d'une majuscule (donc pas d'espace ni de ponctuation)
        if(ord(lettre) >= ord("A") and ord(lettre) <= ord("Z")):
            resultat += lettre
            
    return resultat
            
def Vigenere(message, c):
    cypher = ""
    
    #le texte à chiffrer et la clé doivent etre en majuscule et sans espace ni ponctuation
    message = supprime_accents_minuscules_ponctuations(message)
    c = supprime_accents_minuscules_ponctuations(c)
    
    key = ""
    for i in range(len(message)):
        # Répéter les lettres de la clé jusqu'à atteindre la longueur du texte.
        key += c[i % len(c)]
    
    try:
        #parcourir la longueur du texte à chiffrer
        for i in range(len(message)):

            decalage =  ord(key[i]) - ord("A") # position de la lettre actuelle de la clé dans l'alphabet

            #pour chaque lettre du texte, décaler selon le décalage calculé juste avant puis l'ajouter au résultat
            cypher += CesarLettre(message[i], decalage)
    
    except Exception as e:
        raise Exception(e)
            
    return cypher

def Playfair(message, k):
    
    #le message à chiffrer et la clé doivent etre en majuscule sans espace ni ponctuation
    message = supprime_accents_minuscules_ponctuations(message)
    k = supprime_accents_minuscules_ponctuations(k)
    
    #on remplace les J par des I dans le message et la clé
    message = message.replace("J", "I") 
    k = k.replace("J", "I")
    
    #Fonction pour creer une matrice en utilisant la clé
    def creerMatrice(k):
        M = ""
        
        #Remplir la matrice avec la clé (tout en évitant d'introduire des caractréres déja insérés (exp: SECURITE --> SECURIT))
        for c in k:
            if c not in M:
                M += c
    
        #Completer avec le reste de l'alphabet
        for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if c not in M:
                M += c
    
        # Créer une Matrice 5x5
        grille = [list(M[i:i+5]) for i in range(0, 25, 5)]
        return grille
    
    #Ajoute des 'X' au milieu de lettres doubles du texte et à la fin s'il est impaire
    def Correction(texte):
        resultat = "" #chaine vide
        i = 0
        
        #Parcourir la longueur du texte
        while i < len(texte):
            a = texte[i]
            b = texte[i+1] if i+1 < len(texte) else "X"
            
            #Si 2 lettres sont egales, on ajoute "X" entre elles
            if a == b:
                resultat += a + "X"
                i += 1
            else:
                resultat += a + b
                i += 2
        
        #si la longueur du texte est toujours impaire, on ajoute 'X' à la fin
        if len(resultat) % 2 != 0:
            resultat += "X"
            
        return resultat
    
    #cette focntion retourne la position(ligne, colonne) d'une lettre dans la matrice M
    def position(M, lettre):
        for i in range(5):
            for j in range(5):
                if M[i][j] == lettre:
                    return i, j
         
        #ne retourne rien en cas de non-correspondanse
        return None, None

    plaintext = Correction(message) #correction du message (ajout des 'X')
    M = creerMatrice(k)
    cyphertext = ""
    i = 0
    
    #Parcourir le message
    while i < len(plaintext):
        x , y = plaintext[i] , plaintext[i+1]   #récuperer une paire de lettres (X,Y)
        ligne1 , col1 = position(M, x)          #coordonnées de X dans la matrice
        ligne2 , col2 = position(M, y)          #coordonnées de Y dans la matrice
        
        #meme ligne
        if ligne1 == ligne2:
            cyphertext += M[ligne1][(col1+1) % 5]   #Décalage à Droite (si la fin de la ligne est atteinte, on revient tout à gauche)
            cyphertext += M[ligne2][(col2+1) % 5]
        
        #meme colonne  
        elif col1 == col2:
            cyphertext += M[(ligne1+1) % 5][col1]   #Décalage en Bas (si la fin de la colonne est atteinte, on revient tout en haut)
            cyphertext += M[(ligne2+1) % 5][col2]
            
        #rectangle
        else:
            cyphertext += M[ligne2][col1]
            cyphertext += M[ligne1][col2]           #Récuperer les points opposés
            
        i += 2 #Avancer de 2 caracteres (une paire)
        
    return cyphertext
        
def Polybe(message, k):
       
    #le message à chiffrer et la clé doivent etre en majuscule sans espace ni ponctuation
    message = supprime_accents_minuscules_ponctuations(message)
    k = supprime_accents_minuscules_ponctuations(k)
    
    #on remplace les J par des I dans le message et la clé
    message = message.replace("J", "I") 
    k = k.replace("J", "I")
    
    
    #Fonction pour creer une matrice en utilisant la clé
    def creerMatrice(k):
        M = ""
        
        #Remplir la matrice avec la clé (tout en évitant d'introduire des caractréres déja insérés (exp: SECURITE --> SECURIT))
        for c in k:
            if c not in M:
                M += c
    
        #Completer avec le reste de l'alphabet
        for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
            if c not in M:
                M += c
    
        # Créer une M 5x5
        grille = [list(M[i:i+5]) for i in range(0, 25, 5)]
        return grille
    
    #cette focntion retourne la position(ligne, colonne) d'une lettre dans la matrice M
    def position(M, lettre):
        for i in range(5):
            for j in range(5):
                if M[i][j] == lettre:
                    return i, j
                
        return None, None

    cyphertext = ""
    M = creerMatrice(k)
    
    #Parcours du texte
    for lettre in message:
        x , y = position(M, lettre) # recuperer la position (ligne, colonne) de la lettre courante dans la matrice
        cyphertext += str(x+1) + str(y+1)   # ajouter les coordonnées au resultat ((x+1) car l'indice de la matrice commence par 0)
                
    return cyphertext

"""
plain = "Demain c'est le grand jour"
key = "Gymnastique"

cypher = Vigenere(plain, key)
print("\nVIGENERE:\n Clair: {} \t k: {} \t Cypher: {} " .format(plain, key, cypher))

cypher = Playfair(plain, key)
print("\nPLAYFAIR:\n Clair: {} \t k: {} \t Cypher: {} " .format(plain, key, cypher))

cypher = Polybe(plain, key)
print("\nPOLYBE:\n Clair: {} \t k: {} \t Cypher: {} " .format(plain, key, cypher))

"""