import pygame
import sys
from environnement import *
from horloge import *
from affichage import *
import time
import controleur

# Initialisation de Pygame
pygame.init()

# Création de l'environnement et d'un véhicule
environnement = Environnement()
controleur = controleur.Controleur(environnement.vehicule, environnement)

temps = Horloge()


# Affiche l'écran d'instructions avant de commencer
afficher_instructions()
# Attendre que l'utilisateur appuie sur une touche pour commencer
controleur.gerer_affichage()

# Boucle principale de la simulation
clock = pygame.time.Clock()
temps.demarrer()

while True:

    
    # Gestion des contrôles utilisateur
    controleur.gerer_evenements()


    environnement.vehicule.bouger(temps.get_temps_ecoule())
    collision = environnement.collision()
    la = 0
    while(collision):
        environnement.correction_apres_collision(collision)
        collision = environnement.collision()
        la=1
    if la == 1 :
        environnement.arrete()
        la=0
    temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    afficher(screen, environnement.vehicule, ROUGE, NOIR, environnement.objects, environnement)
    clock.tick(60)

temps.arreter()