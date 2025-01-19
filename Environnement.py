import pygame

class Environnement:

    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def mise_a_jour(self, vehicule):
        # Arrêter le véhicule si proche du bord droit
        if vehicule.x + 17 > self.largeur or vehicule.y  - 17 < 0:  # 25 est le rayon du cercle
            vehicule.arret()

    def afficher(self, screen, vehicule, couleur_vehicule, couleur_texte):
        # Afficher le véhicule
        pygame.draw.circle(screen, couleur_vehicule, (vehicule.x, vehicule.y), 10)

        # Afficher la vitesse
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {vehicule.vitesse*2} m/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))
