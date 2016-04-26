# -*-coding:Utf-8 -*

import game.grille as g
import config.config as c

TAILLE_MAX = c.TAILLE_GRILLE_MAX
TAILLE_MIN = c.TAILLE_GRILLE_MIN


class Jeu:
    """Classe permettant la gestion de la partie"""
    
    def __init__(self, taille=0, grille=[], casesCreusees = set(),\
                       drapeauxPlantes = set(), dicoGeneral = {}):
        self.taille = taille
        
        if self.taille == 0: #On réinitialise les paramètres du jeu
            while 1: #On choisis la taille de la grille
                try:
                    self.taille = int(input(\
                     "Entrer la taille de la grille ({} - {}) : "\
                     .format(TAILLE_MIN, TAILLE_MAX)))
                    if self.taille in range(TAILLE_MIN, TAILLE_MAX):
                        break
                except:
                    continue
            self.plateau = g.Grille(self.taille) #Création de la grille
            self.plateau.cases_minees() # Implantation des mines
            self.plateau.cases_non_minees() #Analyse des cases non minées
            
        else: #On prend les paramètres chargés (entrés dans __init__)
            self.plateau = g.Grille(self.taille) #Création de la grille
            #On remplace les paramètres par ceux sauvegardés
            self.plateau.casesCreusees = casesCreusees
            self.plateau.drapeauxPlantes = drapeauxPlantes
            self.plateau.grille = grille
            self.plateau.dicoGeneral = dicoGeneral
        #Affichage de la grille vide avant le 1er tour
        self.plateau.affichage_grille()
        
    def tour(self):
        """Gère un tour de la partie"""
        
        while 1: #Demande à l'utilisateur de l'action à exécuter
            action = input("\nPlanter un drapeau ou creuser (d/c) : ")
            try:
                if action.lower() in ('d', 'c'):
                    action = action.lower()
                    break
            except:
                continue
        #Demande à l'utilisateur des coordonnées de l'action à exécuter
        while 1:
            coordonnees = input("Coordonnées (ligne, colonne) : ")
            
            try: #-1 car l'utilisateur commence à la ligne 1
                coord = (int(coordonnees.split(",")[0]) - 1,\
                         int(coordonnees.split(",")[1]) - 1)
                if 0 <= coord[0] < self.taille\
                and 0 <= coord[1] < self.taille: #Si coord in grille
                    break
                else:
                    print("Coordonnées hors grille.")
                    continue
            except:
                print("Entrez ligne, colonne séparés par une virgule.")
                continue
        
        if action == 'c': #Si on creuse
            if coord in self.plateau.drapeauxPlantes: #Sur drapeau
                self.plateau.retirer_drapeau(*coord)
            
            elif self.plateau.dicoGeneral[coord] == g.MINE: #Sur mine
                return self.perdu(*coord)
            
            elif coord in self.plateau.casesCreusees: #Sur case creusée
                print("Vous avez déjà creusé ici.")
            
            else: #Sur case non minée
                self.plateau.creuser(*coord)
        
        elif action == 'd': #Si on plante un drapeau
            if (coord in self.plateau.drapeauxPlantes): #Sur drapeau
                self.plateau.retirer_drapeau(*coord)
            
            elif coord in self.plateau.casesCreusees: #Sur case creusée
                print("La case à déjà été creusée")
            
            else: #Sur une case lambda
                self.plateau.placer_drapeau(*coord)
        
        # Si le nb cases creusées + nb mines = nb cases total => gagné
        if len(self.plateau.casesCreusees)\
               + self.plateau.nbMines\
               == self.taille ** 2:
            return self.gagne()
        
        self.plateau.affichage_grille() #Grille affichée en fin de tour
    
    def perdu(self, *coord):
        """Gère le moment où le joueur perd"""
        self.plateau.affichage_grille_minee(*coord)
        print("Dommage ! C'étais une mine !")
        return "perdu"
    
    def gagne(self):
        """Gère le moment où le joueur gagne"""
        self.plateau.affichage_grille()
        print("Aucune mine n'a explosé, mission réussie !")
        return "gagné"
    
    def regles(self):
        """Affiche les règles du jeu"""
        print("LE DEMINEUR est un jeu dans lequel vous devez trouver \
               les mines dispersées dans un champs.", "Pour gagner, vous \
               devez creuser sur toutes les cases n'étant pas des mines. \
               Mais si vous creusez sur une mine, c'est perdu.", "Quand \
               vous creusez, une case indique le nombre de mines aux \
               alentours.", "Vous pouvez planter un drapeau là où vous \
               pensez qu'il y a une mine pour vous en rappeler.", "Si vous \
               voulez l'enlever, il suffit juste de creuser dessus ou d'y \
               planter un second drapeau.", sep = "\n", end = "\n\n")
