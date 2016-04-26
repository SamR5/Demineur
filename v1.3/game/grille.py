# -*-coding:Utf-8 -*

import random as r
import config.config as c


#--------------------Paramètres de base--------------------
# 
#Symbols
TERRAIN = c.TERRAIN
DRAPEAU = c.DRAPEAU
MINE = c.MINE
MINE_EXPLOSE = c.MINE_EXPLOSE
ISOLEE = c.ISOLEE

#Constantes
POURCENTAGE = c.POURCENTAGE
#---------------------------------------------------------------


class Grille:
    """Classe représentant le champs de mine"""
    
    def __init__(self, taille):
        self.taille = taille #Taille de la grille (un carré)
        self.grille = [(' ' + TERRAIN + ' ')\
                       * self.taille]\
                       * self.taille #Carré taille*taille
        self.nbMines = int((self.taille ** 2) * POURCENTAGE)
        self.casesVoisines = ((0, 1), (1, 1), (1, 0),\
                              (1, -1),(0, -1), (-1, -1),\
                              (-1, 0), (-1, 1)) #voisines de (0, 0)
        self.casesCreusees = set()
        self.drapeauxPlantes = set()
        
        #Dictionnaire les objets cachés coordonees:objet
        self.dicoGeneral = {}
        for i in range(self.taille):
            for j in range(self.taille):
                self.dicoGeneral[(i, j)] =  ''
    
    def __repr__(self):
        return "Grille de {0}x{0} contenant {1} mines"\
               .format(self.taille, self.nbMines)
        
    def __str__(self):
        return __repr__(self)
        
    def affichage_grille(self):
        """Affiche la grille à l'utilisateur"""
        for i in self.grille:
            print(i)
    
    def cases_minees(self):
        """Génère de manière aléatoire les coordonnées des mines"""
        mine_count = 0
        #Tant qu'il manque des mines on en ajoute
        while mine_count < self.nbMines:
            coor_mine = (r.randrange(self.taille),\
                         r.randrange(self.taille))
            #Si la mine est deja dedans on passe
            if self.dicoGeneral[coor_mine] == MINE:
                continue
            else: #Sinon on l'ajoute
                self.dicoGeneral[coor_mine] = MINE
                mine_count += 1
    
    def mines_proches(self, ligne, colonne):
        """Retourne le nombre de mines autour de la case"""
        mines_voisines = 0
        for i, j in self.casesVoisines:
            #Si la voisine est dans la grille puis que c'est une mine
            if ligne + i in range(self.taille)\
            and colonne + j in range(self.taille):
                if self.dicoGeneral[(ligne+i, colonne+j)] == MINE:
                    mines_voisines += 1
        return mines_voisines
    
    def cases_non_minees(self):
        """Remplis dicoGeneral pour les cases non minées"""
        for i in range(self.taille):
            for j in range(self.taille):
                #Si c'est une mine inutile de vérifier les alentours
                if self.dicoGeneral[(i, j)] != MINE: 
                    mines_voisines = self.mines_proches(i, j)
                    if mines_voisines == 0: #Si elle est isolée
                        self.dicoGeneral[(i,j)] = ISOLEE
                    elif mines_voisines != 0:
                        self.dicoGeneral[(i, j)] = str(mines_voisines)
    
    def creuser(self, ligne, colonne):
        """Creuse une case de la grille"""
        #On ajoute les coordonnées dans les cases creusées
        self.casesCreusees.add((ligne, colonne))
        nouvelle_ligne = list(self.grille[ligne])
        
        #Si il y a des mines à proximité
        if self.dicoGeneral[(ligne, colonne)] != ISOLEE: 
            nouvelle_ligne[(colonne * 3) + 1]\
            = self.dicoGeneral[(ligne, colonne)] #Ajout de la valeur
            self.grille[ligne] = "".join(nouvelle_ligne)
        
        #Si c'est une case isolée
        else:
            nouvelle_ligne[(colonne * 3) + 1]\
            = self.dicoGeneral[(ligne, colonne)] #Ajout de la valeur
            self.grille[ligne] = "".join(nouvelle_ligne)
            #On creuse autour
            #Sauf si elle est hors grille ou deja creusée
            for i, j in self.casesVoisines: 
                if ligne + i in range(self.taille)\
                and colonne + j in range(self.taille)\
                and (ligne + i, colonne + j) not in self.casesCreusees:
                    self.creuser(ligne + i, colonne + j)
    
    def placer_drapeau(self, ligne, colonne):
        """Place un drapeau sur la case"""
        #On ajoute les coordonnées dans les drapeaux plantés
        self.drapeauxPlantes.add((ligne, colonne)) 
        
        nouvelle_ligne = list(self.grille[ligne])
        nouvelle_ligne[(colonne * 3) + 1] = DRAPEAU
        self.grille[ligne] = "".join(nouvelle_ligne)
    
    def retirer_drapeau(self, ligne, colonne):
        """Retire le drapeau de la case"""
        #On supprime les coordonnées des drapeaux plantés
        self.drapeauxPlantes.discard((ligne, colonne))
        
        nouvelle_ligne = list(self.grille[ligne])
        nouvelle_ligne[(colonne * 3) + 1] = TERRAIN
        self.grille[ligne] = "".join(nouvelle_ligne)
    
    def affichage_grille_minee(self, ligne, colonne):
        """Affiche la grille avec toutes les mines"""
        for i, j in self.dicoGeneral.items():
            if j == MINE:
                #On affiche les mines
                nouvelle_ligne = list(self.grille[i[0]])
                nouvelle_ligne[(i[1] * 3) + 1] = MINE
                self.grille[i[0]] = "".join(nouvelle_ligne)
        #On remodifie la ligne contenant la mine explosée
        nouvelle_ligne = list(self.grille[ligne])
        nouvelle_ligne[(colonne * 3) + 1] = MINE_EXPLOSE
        self.grille[ligne] = "".join(nouvelle_ligne)
        
        return self.affichage_grille()