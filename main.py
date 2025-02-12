import pygame
import sys
from environnement import *
from affichage import *
import time
import controleur


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
    # Gestion des contrôles par l'utilisateur
    controleur.gerer_evenements()

    print(environnement.vehicule.p_centre)
    environnement.bouger()
    environnement.temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    afficher(screen, ROUGE, NOIR, environnement.objects, environnement)
    clock.tick(60)

environnement.vehicule.temps.arreter()