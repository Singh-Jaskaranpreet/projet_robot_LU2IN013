import pygame
import sys
from environnement import *
from horloge import *
from affichage import *
import time
import controleur
from strategy import *

# Initialisation de Pygame
pygame.init()

#temps Création de l'environnement et d'un véhicule
environnement = Environnement()
controleur = controleur.Controleur(environnement.vehicule, environnement)

# Affiche l'écran d'instructions avant de commencer
afficher_instructions()
# Attendre que l'utilisateur appuie sur une touche pour commencer
controleur.gerer_affichage()

# Boucle principale de la simulation
clock = pygame.time.Clock()
environnement.temps.demarrer()

while True:

    controleur.executer_strategie()

    # Gestion des contrôles utilisateur
    controleur.gerer_evenements()


    environnement.bouger(environnement.temps.get_temps_ecoule())
    environnement.temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    afficher(screen, ROUGE, NOIR, environnement.objects, environnement)
    clock.tick(60)

temps.arreter()