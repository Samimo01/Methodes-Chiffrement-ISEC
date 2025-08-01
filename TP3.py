import random

""" BELALOUI SAMY ABDELMADJID - G1 """

#Exo: PGCD et Inverse Modulaire
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a   

def inverseModulaire(a, b):
    if pgcd(a,b) == 1:
        for x in range(1, b):
            if (a * x) % b == 1:
                return x
    else:
        return None

#Exo: Test de Primalité
def primaliteDeterministe(a):
    if a < 2: # 0 ou 1
        return False
    
    if a == 2 or a == 3:
        return True
    
    if a % 2 == 0 or a % 3 == 0: #si c'est un multiple de 2 ou 3
        return False
    
    i = 5
    while i*i <= a: 
        if a % i == 0 or a % (i+2) == 0:
            return False
        i += 6
        
    return True

def MillerRabin(n, k):

    #Verifie la primalite avec des entiers simples
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False

    # n - 1 = 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # tester plusieurs valeurs "a" avec k iterations
    for _ in range(k):
        a = random.randint(2, n - 2)    # 1 < a < n-1
        x = ExpoRapide(a, d, n)  # a^d mod n

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = ExpoRapide(x, 2, n) # x = x^2 mod n
            
            if x == 1:
                return False
            
            if x == n - 1:
                continue

    return True
       
# Chiffement DES
def DES(message, K):
  
    # Verifications des valeurs des parametres
    if any(x not in [0, 1] for x in K):
        raise Exception("(DES): la clé doit etre en format binaire")
    
    if len(message) != 64 or len(K) != 64:
        raise Exception("(DES): Le message et la clé doivent être de 64 bits.")
    
    """
        ETAPES:
    
        - Le message et K doivent etre des listes de 64bits
        - Permutation IP du message
        - Permutation PC-1 pour K (passage à 56bits) ---> K56
        - Diviser le message en 2 parties L et R (32bits chacune)
        
        - Boucle (0, 16):
            - Diviser K56 en 2 parties "C" et "D" (28bits chacune)
            - Décalage à gauche de "C" et "D" [ {1, 2, 9, 16} --> 1 | sinon 2 ]
            - Réassembler "C" et "D"
            
            - Permutation PC-2 pour K56 (passage à 48bits) ---> K48
            
            - Fonction F:
                - Faire Passer R de 32 à 48bits par la matrice E
                - res = XOR (R , K48)
                - diviser res en 8 blocs de 6bits
                - mettre chaque bloc dans un S-box pour passer de 6 à 4bits
                - rassembler le tout pour avoir un res de 32bits
                - faire passer "res" dans la matrice de permutation P
                - L(i) <-- R(i-1)
                - R(i) <-- L(i-1) XOR res
            
        - 32bits swap (L et R) puis rassembler les parties ---> cyphertext
        - Permutation IP^(-1) du cyphertext
        - Retourner cyphertext
    
    """
    
    def diviser32(K):
        return K[:32], K[32:]

    def diviser28(K):
        return K[:28], K[28:]

    def permutation(message, matrice):
        resultat = []
        
        #Parocours de la Matrice
        for ligne in matrice:
            for index in ligne:
                resultat.append(message[index - 1])
                # EXP: matrice[0][0] = 56 ---> resultat[0] = message[55]
                # on utilise (index-1) au lieu de (index) car l'indice de la 1ere case d'une liste = 0 
                
        return resultat

    def decalageGauche(miniK, cpt):
        
        # tour 1, 2, 9, 16 --> décalage de 1
        if cpt in [1, 2, 9, 16] :
            x = miniK.pop(0) #on prend le premier bit pour le placer a la fin
            miniK.append(x)
            
        else: #sinon --> décalage de 2
            x = miniK.pop(0)
            miniK.append(x)
            y = miniK.pop(0)
            miniK.append(y)
            
        return miniK

    def XOR(A, B):
        resultat = []
        
        if(len(A) != len(B)):
            raise Exception("Tailles des tableaux non-égales dans la fonction XOR")
        
        for i in range(0, len(A)):
            if(A[i] == B[i]):
                resultat.append(0)  # 1 XOR 1 = 0 XOR 0 = 0 
            else:
                resultat.append(1)  # 1 XOR 0 = 1
                
        return resultat
    
    def permutationSBOX(bloc, Sbox):
        #bloc: chaine de 6 bits
        #Sbox: matrice 4*16
        
        if(len(bloc) != 6):
            raise Exception("(permutationSbox): le bloc d'entree doit avoir 6 bits")
            
        if len(Sbox) != 4 or any(len(ligne) != 16 for ligne in Sbox):
            raise Exception("(permutationSbox): le Sbox doit etre une matrice de 4*16")
        
        res = []
        
        #ligne: premier + dernier bit
        ligne = [bloc[0], bloc[5]]
        
        #colonne: 2eme:5eme bits 
        colonne = bloc[1 : 5]
        
        #faire passer le num. de la ligne et colonne du binaire au decimal
        ligneD = int("".join(map(str, ligne)), 2)     
        colonneD = int("".join(map(str, colonne)), 2)
        
        #sortir la case du sbox qui correspond
        x = Sbox[ligneD][colonneD]
        
        #conversion en binaire (4bits)
        x = bin(x)[2:].zfill(4)
        
        #mettre les bits dans une liste
        res = [int(bit) for bit in x]
        
        # le resultat est une liste de 4 bits
        return res
        
    def F(R, K48):   
        #E: fait passer R de 32 à 48bits
        E = [
            [32, 1 , 2 , 3 , 4 , 5 ],
            [4 , 5 , 6 , 7 , 8 , 9 ],
            [8 , 9 , 10, 11, 12, 13],
            [12, 13, 14, 15, 16, 17],
            [16, 17, 18, 19, 20, 21],
            [20, 21, 22, 23, 24, 25],
            [24, 25, 26, 27, 28, 29],
            [28, 29, 30, 31, 32, 1 ]
        ]
        
        #P: organise les bits du resultat final
        P = [
            [16, 7 , 20 ,21],
            [29, 12, 28, 17],
            [1 , 15, 23, 26],
            [5 , 18, 31, 10],
            [2 , 8 , 24, 14],
            [32, 27, 3 , 9 ],
            [19, 13, 30, 6 ],
            [22, 11, 4 , 25]
        ]
        
        #Sbox: apres avoir fragmente le cyphertext en 8blocs de 6bits on les fait passer dans les Sbox pour les remplacer par des blocs de 4bits
        Sbox = []
        Sbox.append([
            [14, 4 , 13, 1 , 2 , 15, 11, 8 , 3 , 10, 6 , 12, 5 , 9 , 0 , 7 ],
            [0 , 15, 7 , 4 , 14, 2 , 13, 1 , 10, 6 , 12, 11, 9 , 5 , 3 , 8 ],
            [4 , 1 , 14, 8 , 13, 6 , 2 , 11, 15, 12, 9 , 7 , 3 , 10, 5 , 0 ],
            [15, 12, 8 , 2 , 4 , 9 , 1 , 7 , 5 , 11, 3 , 14, 10, 0 , 6 , 13]
        ])  
        Sbox.append([
            [15,  1, 8 , 14, 6 , 11, 3 , 4 , 9 , 7, 2 , 13, 12, 0, 5 , 10],
            [3 , 13, 4 , 7 , 15, 2 , 8 , 14, 12, 0, 1 , 10, 6 , 9, 11, 5 ],
            [0 , 14, 7 , 11, 10, 4 , 13, 1 , 5 , 8, 12, 6 , 9 , 3, 2 , 15],
            [13, 8 , 10, 1 , 3 , 15, 4 , 2 , 11, 6, 7 , 12, 0 , 5, 14, 9 ]
        ])
        Sbox.append([
            [10, 0 , 9 , 14, 6 , 3 , 15, 5 , 1 , 13, 12, 7 , 11, 4 , 2 , 8 ],
            [13, 7 , 0 , 9 , 3 , 4 , 6 , 10, 2 , 8 , 5 , 14, 12, 11, 15, 1 ],
            [13, 6 , 4 , 9 , 8 , 15, 3 , 0 , 11, 1 , 2 , 12, 5 , 10, 14, 7 ],
            [1 , 10, 13, 0 , 6 , 9 , 8 , 7 , 4 , 15, 14, 3 , 11, 5 , 2 , 12]
        ])
        Sbox.append([
            [7 , 13, 14, 3 , 0 , 6 , 9 , 10, 1 , 2 , 8 , 5 , 11, 12, 4 , 15],
            [13, 8 , 11, 5 , 6 , 15, 0 , 3 , 4 , 7 , 2 , 12, 1 , 10, 14, 9],
            [10, 6 , 9 , 0 , 12, 11, 7 , 13, 15, 1 , 3 , 14, 5 , 2 , 8 , 4],
            [3 , 15, 0 , 6 , 10, 1 , 13, 8 , 9 , 4 , 5 , 11, 12, 7 , 2 , 14]
        ])
        Sbox.append([
            [2 , 12, 4 , 1 , 7 , 10, 11, 6 , 8 , 5 , 3 , 15, 13, 0 , 14, 9],
            [14, 11, 2 , 12, 4 , 7 , 13, 1 , 5 , 0 , 15, 10, 3 , 9 , 8 , 6],
            [4 , 2 , 1 , 11, 10, 13, 7 , 8 , 15, 9 , 12, 5 , 6 , 3 , 0 , 14],
            [11, 8 , 12, 7 , 1 , 14, 2 , 13, 6 , 15, 0 , 9 , 10, 4 , 5 , 3]
        ])
        Sbox.append([
            [12, 1 , 10, 15, 9 , 2 , 6 , 8 , 0 , 13, 3 , 4 , 14, 7 , 5 , 11],
            [10, 15, 4 , 2 , 7 , 12, 9 , 5 , 6 , 1 , 13, 14, 0 , 11, 3 , 8],
            [9 , 14, 15, 5 , 2 , 8 , 12, 3 , 7 , 0 , 4 , 10, 1 , 13, 11, 6],
            [4 , 3 , 2 , 12, 9 , 5 , 15, 10, 11, 14, 1 , 7 , 6 , 0 , 8 , 13]
        ])
        Sbox.append([
            [4 , 11, 2 , 14, 15, 0 , 8 , 13, 3 , 12, 9 , 7 , 5 , 10, 6 , 1],
            [13, 0 , 11, 7 , 4 , 9 , 1 , 10, 14, 3 , 5 , 12, 2 , 15, 8 , 6],
            [1 , 4 , 11, 13, 12, 3 , 7 , 14, 10, 15, 6 , 8 , 0 , 5 , 9 , 2],
            [6 , 11, 13, 8 , 1 , 4 , 10, 7 , 9 , 5 , 0 , 15, 14, 2 , 3 , 12]
        ])
        Sbox.append([
            [13, 2 , 8 , 4 , 6 , 15, 11, 1 , 10, 9 , 3 , 14, 5 , 0 , 12, 7],
            [1 , 15, 13, 8 , 10, 3 , 7 , 4 , 12, 5 , 6 , 11, 0 , 14, 9 , 2],
            [7 , 11, 4 , 1 , 9 , 12, 14, 2 , 0 , 6 , 10, 13, 15, 3 , 5 , 8],
            [2 , 1 , 14, 7 , 4 , 10, 8 , 13, 15, 12, 9 , 0 , 3 , 5 , 6 , 11]
        ])

        #faire passer R de 32 à 48bits
        R = permutation(R, E)
        R = XOR(R, K48)
        
        #diviser R en 8blocs de 6bits
        bloc = []
        
        #res: accueillera les sorties des blocs par les S-box (des blocs de 4bits)
        res = []
        resultat = []
        
        for i in range(8):
            #recuperer chaque 6bits de R
            bloc.append(R[i*6:(i+1)*6])
            
            #effectuer une permutation avec un S-box
            res.append(permutationSBOX(bloc[i], Sbox[i]))
            
            #rassembler les blocs res pour en former qu'un seul de 32bits
            resultat += res[i]  
        
        #ordonner le resultat des S-box avec la matrice P
        resultat = permutation(resultat , P)
        
        return resultat
        
    #PC-1 : fait passer la clé principale de 64 à 56bits (une seule fois)
    PC1 = [
        [57, 49, 41, 33, 25, 17, 9 ],
        [1 , 58, 50, 42, 34, 26, 18],
        [10, 2 , 59, 51, 43, 35, 27],
        [19, 11, 3 , 60, 52, 44, 36],
        [63, 55, 47, 39, 31, 23, 15],
        [7 , 62, 54, 46, 38, 30, 22],
        [14, 6 , 61, 53, 45, 37, 29],
        [21, 13, 5 , 28, 20, 12, 4 ]
    ] #56bits
    
    #PC-2 : fait passer la clé principale de 56 à 48bits (aprés le décalage à gauche de K56)
    PC2 = [
        [4 , 17, 11, 24, 1 , 5 ],
        [3 , 28, 15, 6 , 21, 10],
        [23, 19, 12, 4 , 26, 8 ],
        [16, 7 , 27, 20, 13, 2 ],
        [41, 52, 31, 37, 47, 55],
        [30, 40, 51, 45, 33, 48],
        [44, 49, 39, 56, 34, 53],
        [46, 42, 50, 36, 29, 32]
    ] #48bits
    
    #IP (Initial Permutation) : s'applique au plaintext au début du chiffrement
    IP = [
        [58, 50, 42, 34, 26, 18, 10, 2],
        [60, 52, 44, 36, 28, 20, 12, 4],
        [62, 54, 46, 38, 30, 22, 14, 6],
        [64, 56, 48, 40, 32, 24, 16, 8],
        [57, 49, 41, 33, 25, 17, 9 , 1],
        [59, 51, 43, 35, 27, 19, 11, 3],
        [61, 53, 45, 37, 29, 21, 13, 5],
        [63, 55, 47, 39, 31, 23, 15, 7]
    ] #64bits

    #FP (Final Permutation) : s'applique au cyphertext à la fin du chiffrement
    FP = [
        [40, 8, 48, 16, 56, 24, 64, 32],
        [39, 7, 47, 15, 55, 23, 63, 31],
        [38, 6, 46, 14, 54, 22, 62, 30],
        [37, 5, 45, 13, 53, 21, 61, 29],
        [36, 4, 44, 12, 52, 20, 60, 28],
        [35, 3, 43, 11, 51, 19, 59, 27],
        [34, 2, 42, 10, 50, 18, 58, 26],
        [33, 1, 41, 9 , 49, 17, 57, 25]
    ] #64bits
     
    ### DEBUT DE PROGRAMME ###
    
    cypher = []
    
    a = permutation(message, IP)
    K56 = permutation(K, PC1)
    L, R = diviser32(a)
    
    for i in range(16):
        #Operations sur K56
        C , D = diviser28(K56)
        C , D = decalageGauche(C, i+1) , decalageGauche(D, i+1)
        K56 = C + D
        
        #Faire passer K56 à 48bits (K48)
        K48 = permutation(K56, PC2)
        
        #Operation de Feistel
        temp = L
        L = R       # L(i) = R(i-1)
        R = XOR(temp , F(R, K48))   # R(i) = L(i-1) XOR f( R(i-1) , K48 )
        
    #32bits swap + IP^(-1)
    cypher = permutation(R+L , FP)

    # Affichage binaire groupé par octets
    binaire = ''.join(str(bit) for bit in cypher)
    resultat = ' '.join([binaire[i:i+8] for i in range(0, 64, 8)])
    
    return resultat

# Exponentiation rapide
def ExpoRapide(a, b, m):
    # a^b mod m
    
    if(a <= 0 or b < 0 or m <= 0):
        raise Exception("Les valeurs a, b, m doivent etre positives.")
    
    if b == 0:
        return 1
    
    r = 1
    a = a % m
    
    while b > 0:
        if b % 2 == 1:
            r = (r*a) % m
        
        a = (a*a) % m
        b = b // 2
       
    # r = a^b mod m
    return r