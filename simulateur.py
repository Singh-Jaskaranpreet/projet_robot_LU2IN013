import pygame
import sys
from Vehicule import *
from Environnement import *

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1080, 800
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation de Véhicule")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Création de l'environnement et d'un véhicule
environnement = Environnement(LARGEUR, HAUTEUR)
vehicule = Vehicule("Voiture", 200, HAUTEUR // 2, 0, 4)

# Boucle principale
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()
    vehicule.gerer_controles(keys)

    # Mise à jour des éléments
    vehicule.bouger()
    environnement.mise_a_jour(vehicule)

    # Affichage
    screen.fill(BLANC)
    environnement.afficher(screen, vehicule, ROUGE, NOIR)
    pygame.display.flip()
    clock.tick(60)
