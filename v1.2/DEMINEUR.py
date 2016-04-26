# -*-coding:Utf-8 -*

#
#LE DEMINEUR
#
#Codé par RAMI SAMUEL
#VERSION 1.2
#

import os
import game.gestion_partie as j
import save.gestion_fichiers as gf

print("LE DEMINEUR est un jeu dans lequel vous devez trouver \
les mines dispersées dans un champs.", "Pour gagner, vous \
devez creuser sur toutes les cases n'étant pas des mines. \
Mais si vous creusez sur une mine, c'est perdu.", "Quand \
vous creusez, une case indique le nombre de mines aux \
alentours.", "Vous pouvez planter un drapeau là où vous \
pensez qu'il y a une mine pour vous en rappeler.", "Si vous \
voulez l'enlever, il suffit juste de creuser dessus ou d'y \
planter un second drapeau.", sep = "\n", end = "\n\n")

#On charge tout, si il n'y a rien les différents paramètres seront vides
Chargement = gf.GestionFichiers()
Chargement.charger()

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
            p = j.Jeu(taille, grille, casesCreusees,\
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
    
    if resultat == "gagné":
        Chargement.effacer_sauvegarde()
        break
    elif resultat == "perdu":
        Chargement.effacer_sauvegarde()
        break
    else:
        #Veiller à bien maintenir l'ordre des entrées
        Chargement.sauvegarder(p.plateau.casesCreusees,\
                               p.plateau.drapeauxPlantes,\
                               p.plateau.taille,\
                               p.plateau.grille,\
                               p.plateau.dicoGeneral)
        continue

os.system("pause")
