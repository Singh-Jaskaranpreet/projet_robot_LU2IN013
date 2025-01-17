import pygame
import sys
from Vehicule import *

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

# Création d'un véhicule
vehicule = Vehicule("Voiture", 200, HAUTEUR // 2, 0, 4)

# Boucle principale
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Contrôles utilisateur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        vehicule.acceleration(0.5)  # Augmenter la vitesse
    if keys[pygame.K_LEFT]:
        vehicule.deceleration(0.5)  # Réduire la vitesse
    if keys[pygame.K_SPACE]:
        vehicule.arret()  # Arrêter le véhicule

    # Mise à jour du véhicule
    vehicule.bouger()

    # Arrêt si le véhicule est à moins de 10 pixels du bord droit
    if vehicule.x + 25 >= LARGEUR - 10:  # 25 est le rayon du cercle
        vehicule.arret()

    # Affichage
    screen.fill(BLANC)
    pygame.draw.circle(screen, ROUGE, (vehicule.x, vehicule.y), 10)  # Représentation du véhicule sous forme de cercle

    # Affichage de la vitesse
    font = pygame.font.SysFont(None, 36)
    vitesse_text = font.render(f"Vitesse: {vehicule.vitesse*2} m/s", True, NOIR)
    screen.blit(vitesse_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
