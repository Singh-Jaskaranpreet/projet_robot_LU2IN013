import pygame
from math import *

class Environnement:

    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur

    def mise_a_jour(self, vehicule):
        # Arrêter le véhicule si proche du bord droit
        if vehicule.x + 17 > self.largeur or vehicule.y  - 17 < 0 or vehicule.x - 17 < 0 or vehicule.y + 17 > self.hauteur :  # 25 est le rayon du cercle
            vehicule.arret()

    def afficher(self, screen, vehicule, couleur_vehicule, couleur_texte):
        Hauteur = 30
        listP = [[vehicule.x+cos(20)*Hauteur, vehicule.y+sin(20)*Hauteur],[vehicule.x-cos(20)*Hauteur, vehicule.y-sin(20)*Hauteur]]
        pp = pygame.math.Vector2([vehicule.x,vehicule.y])
        rotated_points = [(pygame.math.Vector2(x,y)-pp).rotate(vehicule.angle)+pp for x, y in listP]
        # Points du triangle
        point_Rarr = (vehicule.x, vehicule.y)  # Sommet
        #point_Rgauch = (vehicule.x+cos(vehicule.angle+20)*Hauteur, vehicule.y+sin(vehicule.angle+20)*Hauteur)  # Bas gauche
        point_Rgauch = (rotated_points[1][0],rotated_points[1][1])
        point_Rdroite = (rotated_points[0][0],rotated_points[0][1])
        #point_Rdroite = (vehicule.x+cos(vehicule.angle-20)*Hauteur, vehicule.y+sin(vehicule.angle-20)*Hauteur)  # Bas droite
        # Afficher le véhicule
        pygame.draw.polygon(screen, couleur_vehicule,[point_Rarr,point_Rgauch,point_Rdroite])

        # Afficher la vitesse
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {abs(vehicule.vitesse*2)} m/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))

