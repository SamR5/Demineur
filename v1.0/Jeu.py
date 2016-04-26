# -*-coding:Utf-8 -*

import Grid as G


class Jeu:
    """Classe permettant la gestion du jeu"""
    
    def __init__(self):
        self.Regles()
        choix_niveau = True
        while choix_niveau: #On choisis la taille de la grille
            try:
                self.taille = int(input("Entrer la taille de la grille (5 - 25) : "))
                if self.taille in range(5, 26): #Taille de la grille : entre 5x5 et 25x25
                    choix_niveau = False
            except:
                choix_niveau = True
        
        self.plateau = G.Grille(self.taille) #Création de la grille
        self.plateau.cases_minees() # Implantation des mines
        self.plateau.cases_non_minees() #Analyse des cases non minées
        
    def Tour(self):
        """Gère un tour de la partie"""
        
        self.plateau.affichage_grille() #Affichage de la grille vide au debut du tour
        
        while 1: #Demande à l'utilisateur de l'action à exécuter
            action = input("\nVoulez-vous planter un drapeau (d) ou creuser (c) : ")
            try:
                if action.lower() in ('d', 'c'): #On sort de la boucle si 'c' ou 'C' ou 'd' ou 'D'
                    action = action.lower()
                    break
            except:
                continue
        
        while 1: #Demande à l'utilisateur des coordonnées de l'action à exécuter
            coordonnees = input("Entrez les coordonnées (ligne, colonne) : ")
            
            try: #On met les coordonnées dans un tuple après leur avoir oté 1 car l'utilisateur commence à la ligne 1
                coord = (int(coordonnees.split(",")[0]) - 1, int(coordonnees.split(",")[1]) - 1)
                if 0 <= coord[0] < self.taille and  0 <= coord[1] < self.taille: #Si coord dans la grille on sort de la boucle
                    break
                else:
                    print("Les coordonnées choisies ne sont pas dans la grille.")
                    continue
            except:
                print("Une erreure est survenue, veuillez recommencer.")
                continue
        
        
        if action == 'c': #Si on creuse
            if coord in self.plateau.drapeaux_plantes: #Sur un drapeau
                self.plateau.retirer_drapeau(*coord)
            
            elif self.plateau.dico_general[coord] == G.MINE: #Sur une mine
                return self.Perdu()
            
            elif coord in self.plateau.cases_creusees: #Sur un case déja creusée
                print("Vous avez déjà creusé ici.")
            
            else: #Sur une case lambda non minée
                self.plateau.creuser(*coord)
        
        elif action == 'd': #Si on plante un drapeau
            if (coord in self.plateau.drapeaux_plantes): #Sur un drapeau
                self.plateau.retirer_drapeau(*coord)
            
            elif coord in self.plateau.cases_creusees: #Sur un case déja creusée
                print("La case à déjà été creusée, pas la peine d'y mettre un drapeau")
            
            else: #Sur une case lambda
                self.plateau.placer_drapeau(*coord)
        
        # Si le nombre de cases creusées + nb mines = nb de cases de la grille on gagne
        if len(self.plateau.cases_creusees) + self.plateau.nb_mines == self.taille ** 2:
            return self.Gagne()
        else:
            return self.Tour() #Sinon on rejoue
    
    def Perdu(self):
        """Gère le moment où le joueur perd"""
        self.plateau.affichage_grille_minee()
        print("Dommage ! C'étais une mine !")
    
    def Gagne(self):
        """Gère le moment où le joueur gagne"""
        self.plateau.affichage_grille()
        print("Aucune mine n'a explosé, mission réussie !")
    
    def Regles(self):
        """Affiche les règles du jeu"""
        print("LE DEMINEUR est un jeu dans lequel vous devez trouver les mines dispersées dans un champs.",\
        "Pour gagner, vous devez creuser sur toutes les cases n'étant pas des mines. Mais si vous creusez sur une mine, c'est perdu.",\
        "Quand vous creusez, une case indique le nombre de mines aux alentours.",\
        "Vous pouvez planter un drapeau là où vous pensez qu'il y a une mine pour vous en rappeler.",\
        "Si vous voulez l'enlever, il suffit juste de creuser dessus ou d'y planter un second drapeau", end = "\n\n")
