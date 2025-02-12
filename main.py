import pygame
import sys
import environnement
import affichage
import time
import controleur


# Initialisation de Pygame
pygame.init()

#temps Création de l'environnement et d'un véhicule
environnement = environnement.Environnement()
controleur = controleur.Controleur(environnement.vehicule, environnement)

# Affiche l'écran d'instructions avant de commencer
affichage.afficher_instructions()
# Attendre que l'utilisateur appuie sur une touche pour commencer
controleur.gerer_affichage()

# Boucle principale de la simulation
clock = pygame.time.Clock()
environnement.temps.demarrer()

while True:
    environnement.temps.set_time_scale(10)
    controleur.executer_strategie()
    # Gestion des contrôles par l'utilisateur
    controleur.gerer_evenements()

    environnement.bouger()
    environnement.temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    affichage.afficher(affichage.screen, affichage.ROUGE, affichage.NOIR, environnement.objects, environnement)
    clock.tick(60)

environnement.vehicule.temps.arreter()