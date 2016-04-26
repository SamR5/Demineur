# -*-coding:Utf-8 -*

import random as r


#------------------------------------------------------------------------
# Constantes
TERRAIN = '.'
TERRAIN_ESPACE = ' . '
DRAPEAU = '!'
MINE = '*'
ISOLEE = '/'
PROX = '   '
POURCENTAGE = 0.15
#------------------------------------------------------------------------

"""A debugger : 
    - Si on met un drapeau sur une case isolée et qu'on clique sur sa voisine isolée, maintenir drapeau ou pas ? (actuellement il disparait, tant mieux)
    - Si on met un drapeau sur une case prox et qu'on clique sur sa voisine isolée, maintenir drapeau ou pas ? (actuellement il disparait, tant mieux)
"""

class Grille:
    """Classe représentant le champs de mine"""
    
    def __init__(self, taille):
        self.taille = taille #Taille de la grille (un carré)
        self.grille = [TERRAIN_ESPACE * self.taille] * self.taille #Carré taille*taille
        self.nb_mines = int(round((self.taille ** 2) * POURCENTAGE, 0)) #15% de mines
        self.cases_voisines = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)) #voisines de (0, 0) utilisé pour chercher autour d'une case
        self.cases_creusees = set()
        self.drapeaux_plantes = set()
        
        #Dictionnaire contenant les objets de la grille coordonees:objet
        self.dico_general = {}
        for i in range(self.taille):
            for j in range(self.taille):
                self.dico_general[(i, j)] =  ''
    
    def __repr__(self):
        return "Grille de {0}x{0} contenant {1} mines".format(self.taille, self.nb_mines)
        
    def __str__(self):
        return __repr__(self)
        
    def affichage_grille(self):
        """Affiche la grille à l'utilisateur"""
        for i in self.grille:
            print(i)
    
    def cases_minees(self): #A GENERER AU DEBUT DE LA PARTIE
        """Génère de manière aléatoire les coordonnées des mines sur la grille"""
        mine_count = 0
        while mine_count < self.nb_mines: #Tant qu'il manque des mines on en ajoute
            coor_mine = (r.randrange(self.taille), r.randrange(self.taille))
            if self.dico_general[coor_mine] == MINE: #Si la mine est deja dedans on passe
                continue
            else: #Sinon on l'ajoute
                self.dico_general[coor_mine] = MINE
                mine_count += 1
    
    def mines_proches(self, ligne, colonne): #AUTOMATIQUE
        """Retourne le nombre de mines autour de la case creusée"""
        mines_voisines = 0
        
        for i, j in self.cases_voisines:
            #Si la voisine est dans la grille
            if 0 <= ligne + i < self.taille and 0 <= colonne + j < self.taille: #Si on n'est pas hors de la grille
                if self.dico_general[(ligne + i, colonne + j)] == MINE: #Si c'est une mine
                    mines_voisines += 1
        
        return mines_voisines
    
    def cases_non_minees(self): #A GENERER AU DEBUT DE LA PARTIE
        """Remplis le dico_general avec les caractéristiques des cases n'étant pas des mines"""
        for i in range(self.taille):
            for j in range(self.taille):
                if self.dico_general[(i, j)] != MINE: #Si c'est une mine inutile de vérifier les alentours
                    mines_voisines = self.mines_proches(i, j)
                    if mines_voisines == 0: #Si elle est isolée
                        self.dico_general[(i,j)] = ISOLEE
                    elif mines_voisines != 0: #Si elle a des mines autour
                        self.dico_general[(i, j)] = str(mines_voisines)
    
    def creuser(self, ligne, colonne):
        """Creuse une case de la grille"""
        self.cases_creusees.add((ligne, colonne)) #On ajoute les coordonnées dans les cases creusées
        nouvelle_ligne = list(self.grille[ligne])
            
        if self.dico_general[(ligne, colonne)] != ISOLEE: #Si il y a des mines à proximité
            nouvelle_ligne[(colonne * 3) + 1] = self.dico_general[(ligne, colonne)] #on ajoute la valeur correspondante à la grille
            self.grille[ligne] = "".join(nouvelle_ligne)
            
        else: #Si c'est une case isolée
            nouvelle_ligne[(colonne * 3) + 1] = self.dico_general[(ligne, colonne)] #on ajoute la valeur correspondante à la grille
            self.grille[ligne] = "".join(nouvelle_ligne)
            
            for i, j in self.cases_voisines: #Et on creuse tout autour sauf si la case est deja creusée
                if 0 <= ligne + i < self.taille and 0 <= colonne + j < self.taille and ((ligne + i, colonne + j) not in self.cases_creusees):
                    self.creuser(ligne + i, colonne + j)
    
    def placer_drapeau(self, ligne, colonne):
        """Place un drapeau sur la case"""
        self.drapeaux_plantes.add((ligne, colonne)) #On ajoute dans la liste des drapeaux
        
        nouvelle_ligne = list(self.grille[ligne]) #Changement de la grille affichée
        nouvelle_ligne[(colonne * 3) + 1] = DRAPEAU
        self.grille[ligne] = "".join(nouvelle_ligne)
    
    def retirer_drapeau(self, ligne, colonne):
        """Retire le drapeau de la case"""
        self.drapeaux_plantes.discard((ligne, colonne)) #On supprime de la liste des drapeaux
        
        nouvelle_ligne = list(self.grille[ligne]) #Changement de la grille affichée
        nouvelle_ligne[(colonne * 3) + 1] = TERRAIN
        self.grille[ligne] = "".join(nouvelle_ligne)
    
    def affichage_grille_minee(self):
        """Affiche la grille avec toutes les mines (qd on perd)"""
        for i, j in self.dico_general.items():
            if j == MINE:
                nouvelle_ligne = list(self.grille[i[0]]) #Décomposition, ajout d'une mine puis recomposition 
                nouvelle_ligne[(i[1] * 3) + 1] = MINE #i = (ligne, colonne)
                self.grille[i[0]] = "".join(nouvelle_ligne)
        
        return self.affichage_grille()