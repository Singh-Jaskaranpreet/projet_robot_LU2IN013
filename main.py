import pygame
import sys
from src.modele import Environnement,Vehicule
from src.affichage import Affichage
from src.controleur import Controleur
import time
import random as r
#import threading
#import lcm 



#temps Création de l'environnement et d'un véhicule
environnement = Environnement()
controleur = Controleur(environnement.vehicule, environnement)
affichage = Affichage(1200,800)

# Affiche l'écran d'instructions avant de commencer
affichage.afficher_instructions()
# Attendre que l'utilisateur appuie sur une touche pour commencer
controleur.gerer_affichage()

#threading.Thread(target=lcm.lire_commandes, args=(environnement,), daemon=True).start()

# Boucle principale de la simulation
clock = pygame.time.Clock()
environnement.temps.demarrer()
x=0
while True:
    while x > 8 :
        affichage.couleurs[3]=r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)
        x=0
    x+=1
    environnement.temps.set_time_scale(1)
    controleur.executer_strategie()
    # Gestion des contrôles par l'utilisateur
    controleur.gerer_evenements()

    environnement.bouger()
    environnement.temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    affichage.afficher(environnement.objects, environnement)
    clock.tick(60)*environnement.temps.time_scale

environnement.temps.arreter()