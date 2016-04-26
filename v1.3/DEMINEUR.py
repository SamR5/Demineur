# -*-coding:Utf-8 -*

#
#LE DEMINEUR
#
#Codé par RAMI SAMUEL
#VERSION 1.3
#

import os
import game.gestion_partie as j
import save.gestion_fichiers as gf

print("LE DEMINEUR est un jeu dans lequel vous devez trouver \
les mines dispersées dans un champs. Pour gagner, vous devez \
creuser sur toutes les cases non minées. Mais si vous creusez \
sur une mine, c'est perdu. Quand vous creusez, une case indique \
le nombre de mines aux alentours. Vous pouvez planter un drapeau \
là où vous pensez qu'il y a une mine pour vous en rappeler. Si vous \
voulez l'enlever, il suffit juste de creuser dessus ou d'y planter \
un second drapeau.\n\nAppuyez à tout moment sur r/q pour \
recommencer ou quitter", end = "\n\n")

#On charge dictionnaire des données
Chargement = gf.GestionFichiers()
Chargement.charger()
#Puis on affecte aux différentes variables les données sauvegardées
continuer = Chargement.dicoDesDonnees["continuer"]
taille = Chargement.dicoDesDonnees["taille"]
grille = Chargement.dicoDesDonnees["grille"]
casesCreusees = Chargement.dicoDesDonnees["casesCreusees"]
drapeauxPlantes = Chargement.dicoDesDonnees["drapeauxPlantes"]
dicoGeneral = Chargement.dicoDesDonnees["dicoGeneral"]

#Si il y a une sauvegarde
while continuer: 
    try:
        continuer = input("'o' pour continuer la partie précédente, sinon Entrée : ")
        if continuer.lower() == 'o':
            p = j.Jeu(taille, grille, casesCreusees,
                      drapeauxPlantes, dicoGeneral) #Attention à maintenir l'ordre
            break
        else:
            p = j.Jeu()
            break
    except:
        print("Une erreur c'est produite, réessayez.", end="\n\n")
        continuer = True

#Si il n'y a pas de sauvegarde
if not continuer:
    p = j.Jeu()


while 1:
    resultat = p.tour()
    
    if resultat is "gagné": #Si l'utilisateur gagne
        Chargement.effacer_sauvegarde()
        break
    elif resultat is "perdu": #Si l'utilisateur perd
        Chargement.effacer_sauvegarde()
        break
    elif resultat is "recommencer": #Si l'utilisateur recommence
        a = input("Etes-vous sur de vouloir recommencer ? "
                  +"La sauvegarde sera écrasée (o/n) : ")
        if a in ('o', 'O'): #Si il veut vraiement
            Chargement.effacer_sauvegarde()
            p = j.Jeu()
            continue
        else: #Si il change d'avis
            continue
    elif resultat is "quitter": #Si l'utilisateur quitte
        a = input("Etes-vous sur de vouloir quitter ? (o/n) ")
        if a in ('o', 'O'): #Si il veut vraiement
            break #Pas de sauvegarde car tour non réalisé
        else: #Si il change d'avis
            continue
    else: #Sinon on continue la partie après l'avoir sauvegardée
        #Veiller à bien maintenir l'ordre des entrées
        Chargement.sauvegarder(p.plateau.casesCreusees,
                               p.plateau.drapeauxPlantes,
                               p.plateau.taille,
                               p.plateau.grille,
                               p.plateau.dicoGeneral)
        continue

os.system("pause")
