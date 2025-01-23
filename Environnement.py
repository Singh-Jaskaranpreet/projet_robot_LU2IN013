import pygame
import math

class Environnement:

    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def mise_a_jour(self, vehicule):
        # Arrêter le véhicule si proche du bord droit
        if vehicule.x + 17 > self.largeur or vehicule.y  - 17 < 0 or vehicule.x - 17 < 0 or vehicule.y + 17 > self.hauteur :  # 25 est le rayon du cercle
            vehicule.arret()

    def afficher(self, screen, vehicule, couleur_vehicule, couleur_texte):
               # Afficher le véhicule
        pygame.draw.polygon(screen, couleur_vehicule,[vehicule.r_Ar,vehicule.r_Avg,vehicule.r_Avd])

        # Afficher la vitesse
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {abs(vehicule.vitesse*2)} m/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))

