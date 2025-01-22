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
        # Points du triangle
        (x,y)=(vehicule.x,vehicule.y)
        (xg,yg)=(x+vehicule.long*2,y-(vehicule.long//2))
        (xd,yd)=(x+vehicule.long*2,y+(vehicule.long//2))
        point_Rarr = (x, y)  # Sommet
        point_Rgauch = (x+(xg-x)*math.cos(vehicule.angle)-(yg-y)*math.sin(vehicule.angle),y+(xg-x)*math.sin(vehicule.angle)+(yg-y)*math.cos(vehicule.angle))  # Bas gauche
        point_Rdroite = (x+(xd-x)*math.cos(vehicule.angle)-(yd-y)*math.sin(vehicule.angle),y+(xd-x)*math.sin(vehicule.angle)+(yd-y)*math.cos(vehicule.angle))  # Bas droite
        # Afficher le véhicule
        pygame.draw.polygon(screen, couleur_vehicule,[point_Rarr,point_Rgauch,point_Rdroite])

        # Afficher la vitesse
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {abs(vehicule.vitesse*2)} m/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))

