# Chiffrement Classique et Moderne en Python

Projet Python pour expérimenter différents algorithmes de chiffrement classiques et modernes.

## Fonctionnalités

- Chiffrement César (et déchiffrement par force brute)
- Chiffrement Vigenère
- Chiffrement Playfair
- Chiffrement Polybe
- Chiffrement DES (Data Encryption Standard)
- Exponentiation rapide (modulaire)
- Calcul du PGCD et de l’inverse modulaire
- Test de primalité (déterministe et Miller-Rabin)

## Structure du projet
- main.py:  Menu principal et gestion des interactions utilisateur 
- TP2.py:   Fonctions de chiffrement classiques (César, Vigenère, Playfair, Polybe) 
- TP3.py:   Fonctions avancées (DES, exponentiation rapide, primalité, PGCD)

## Utilisation

1. Lancer le programme principal :
   ```bash
   python main.py
2. Suivre le menu pour choisir l’algorithme ou l’opération souhaitée.
3. Saisir les messages et clés demandés.

## Détail des modules
### TP2.py
- CesarTexte : Chiffre un texte par la méthode de César.
- ForceBrute : Déchiffre un texte chiffré par César en testant toutes les clés.
- Vigenere : Chiffre un texte avec la méthode de Vigenère.
- Playfair : Chiffre un texte avec la méthode de Playfair (carré 5x5).
- Polybe : Chiffre un texte avec la méthode de Polybe (conversion en coordonnées).
- supprime_accents_minuscules_ponctuations : Nettoie le texte pour le chiffrement.

### TP3.py
- pgcd : Calcule le plus grand commun diviseur.
- inverseModulaire : Calcule l’inverse modulaire.
- primaliteDeterministe : Teste la primalité d’un nombre (méthode simple).
- MillerRabin : Teste la primalité (méthode probabiliste).
- ExpoRapide : Exponentiation rapide modulaire.
- DES : Implémentation complète du chiffrement DES (avec permutations, S-box, gestion des clés, etc.).

### main.py
- Menu interactif pour accéder à toutes les fonctionnalités.
- Conversion automatique des messages/clefs pour DES.
- Gestion des erreurs et des entrées utilisateur.
