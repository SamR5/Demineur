# -*-coding:Utf-8 -*

import os

listeParaRecup = []
with open("config"+os.sep+"parametres.txt", "r") as para:
    for ligne in para:
        listeParaRecup.append(ligne)

listePara = []
for i in listeParaRecup:
    listePara.append(i.split("'"))

#On prend -2 car chaque ligne finit par : '\n
#Pour les symbols
TERRAIN = listePara[0][-2]
DRAPEAU = listePara[1][-2]
MINE = listePara[2][-2]
MINE_EXPLOSE = listePara[3][-2]
ISOLEE = listePara[4][-2]

#Pour les valeurs numériques
POURCENTAGE = float(listePara[5][-2])
TAILLE_GRILLE_MIN = int(listePara[6][-2])
TAILLE_GRILLE_MAX = int(listePara[7][-2])