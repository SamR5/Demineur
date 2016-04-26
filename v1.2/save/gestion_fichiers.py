# -*-coding:Utf-8 -*

import pickle
import os


class GestionFichiers:
    """Classe permettant la gestion des fichiers"""
    
    def __init__(self):
        self.continuer = False
        self.dicoDesDonnees = {}
    
    def sauvegarder(self, casesCreusees, drapeauxPlantes,\
                    taille, grille, dicoGeneral):
        """Sauvegarde les différents paramètres de la
        partie dans un dictionnaire"""
        
        self.dicoDesDonnees = {
        "continuer":True, 
        "casesCreusees":casesCreusees, 
        "drapeauxPlantes":drapeauxPlantes, 
        "taille":taille, 
        "grille": grille, 
        "dicoGeneral":dicoGeneral
        }
        with open("save"+os.sep+"sauvegarde", 'wb') as save:
            monPickler = pickle.Pickler(save)
            monPickler.dump(self.dicoDesDonnees)
        
    def effacer_sauvegarde(self):
        """Efface la sauvegarde quand on gagne, perd ou recommence"""
        self.dicoDesDonnees = {
        "continuer":False, 
        "casesCreusees":set(), 
        "drapeauxPlantes":set(), 
        "taille":0, 
        "grille": [], 
        "dicoGeneral":{}
        }
        with open("save"+os.sep+"sauvegarde", 'wb') as save:
            monPickler = pickle.Pickler(save)
            monPickler.dump(self.dicoDesDonnees)
    
    def charger(self):
        """Charge les données sauvegardées"""
        with open("save"+os.sep+"sauvegarde", 'rb') as save:
            monDepickler = pickle.Unpickler(save)
            self.dicoDesDonnees = monDepickler.load()
            
            self.continuer = self.dicoDesDonnees["continuer"]
            self.casesCreusees = self.dicoDesDonnees["casesCreusees"]
            self.drapeauxPlantes = self.dicoDesDonnees["drapeauxPlantes"]
            self.taille = self.dicoDesDonnees["taille"]
            self.grille = self.dicoDesDonnees["grille"]
            self.dicoGeneral = self.dicoDesDonnees["dicoGeneral"]