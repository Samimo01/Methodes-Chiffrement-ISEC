from TP2 import *
from TP3 import *
import os

""" BELALOUI SAMY ABDELMADJID - G1 """

#affichage des options
def afficherMenu():
    print(" 1. Chiffrement César")
    print(" 2. Déchiffrment par Force Brute (César)")
    print(" 3. Chiffrement Playfair")
    print(" 4. Chiffrement Polybe")
    print(" 5. Chiffrement Vigenére")
    print(" 6. Chiffrement DES")
    print(" 7. Exponentiation Rapide")
    print(" 8. Quitter")

#Convertit une chaîne en liste de 64 bits (DES)
def conversion64bits(texte):

    bits = []
    for c in texte:
        bits.extend([int(b) for b in format(ord(c), '08b')])
    # Ajuste à 64 bits
    if len(bits) < 64:
        bits += [0] * (64 - len(bits))
    else:
        bits = bits[:64]
    return bits

#Menu principal
def main():
    while True:
        os.system('cls')
        afficherMenu()
        
        try:
            choix = int(input("\n Votre choix: "))
        except ValueError:
            print(" Erreur, le choix doit être un entier.")
            input(" Appuyez sur une touche...")
            continue

        try:
            #Cesar
            if choix == 1:
                print(" Vous avez choisi: César \n")
                message = input(" Veuillez saisir votre message à chiffrer: ")
                
                while True:
                    try:
                        cle = int(input(" Veuillez saisir votre clé (1-25): "))
                        if 1 <= cle <= 25:
                            break
                        
                    except Exception:
                        raise Exception(" la clé doit être un entier.")
                        
                cypher = CesarTexte(message, cle)
                print(" Résultat :", cypher)

            #Force Brute
            elif choix == 2:
                print(" Vous avez choisi: Force Brute \n")
                message = input(" Veuillez saisir votre message à déchiffrer: ")
                
                ForceBrute(message)

            #Playfair
            elif choix == 3:
                print(" Vous avez choisi: Playfair \n")
                message = input(" Veuillez saisir votre message à chiffrer: ")
                cle = input(" Veuillez saisir votre clé: ")
                cypher = Playfair(message, cle)
                print(" Résultat :", cypher)

            #Polybe
            elif choix == 4:
                print(" Vous avez choisi: Polybe \n")
                message = input(" Veuillez saisir votre message à chiffrer: ")
                cle = input(" Veuillez saisir votre clé: ")
                cypher = Polybe(message, cle)
                print(" Résultat :", cypher)

            #Vigenere
            elif choix == 5:
                print(" Vous avez choisi: Vigenere \n")
                message = input(" Veuillez saisir votre message à chiffrer: ")
                cle = input(" Veuillez saisir votre clé: ")
                cypher = Vigenere(message, cle)
                print(" Résultat :", cypher)

            #DES
            elif choix == 6:
                print(" Vous avez choisi: DES \n")
                message = input(" Veuillez saisir votre message (max 8 caractères): ")
                cle = input(" Veuillez saisir votre clé (max 8 caractères): ")
                
                if len(message) > 8 or len(cle) > 8:
                    raise Exception(" la longueur du message et de la clé ne doivent pas dépasser 8 caractères.")
                
                message_bin = conversion64bits(message)
                cle_bin = conversion64bits(cle)
                cypher = DES(message_bin, cle_bin)
                print(" Résultat :", cypher)

            #Exponentiation Rapide
            elif choix == 7:
                print(" Vous avez choisi: Exponentiation Rapide \n")
                a = int(input(" a = "))
                b = int(input(" b = "))
                m = int(input(" m = "))
                r = ExpoRapide(a, b, m)
                
                print(" a^b mod m = {}" .format(r))

            #Quitter
            elif choix == 8:
                rep = input(" Confirmer (y/N)? ")
                if rep.lower() == 'y': # si "oui", sortir de la boucle
                    break
                else:
                    continue
            
            else:
                print(" Choix invalide.")

        except Exception as e:
            print(" Erreur:", e)

        input(" Appuyez sur une touche...")
        
    input("\n Fin de Programme...")

if __name__ == "__main__":
    main()