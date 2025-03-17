import pygame
from .environnement import Environnement
import math as m
#LARGEUR, HAUTEUR = 1200, 800

# Initialisation de Pygame
pygame.init()

def echelle(x):
     return  round(0.003*x,3)

class Affichage:
    # Dimensions de la fenêtre
    def __init__(self,largeur,hauteur):
         self.largeur=largeur
         self.hauteur=hauteur
         self.screen = pygame.display.set_mode((largeur,hauteur))
         self.couleurs = [(255,255,255),(0,0,0),(255,0,0),(0,0,0)] #Blanc,Noir,Rouge
        


    def afficher(self, objects, environnement):
            """
            Affiche l'environnement, y compris le véhicule, les objets (obstacles),
            et la vitesse du véhicule.
            """
            pygame.display.set_caption("Simulation de Véhicule")


            self.screen.fill(self.couleurs[0]) # Remplir l'écran en blanc

            # Afficher le véhicule sous forme de triangle
            points_triangle = environnement.vehicule.position_des_roues(environnement.vehicule.p_centre)
            pygame.draw.polygon(self.screen, self.couleurs[2], points_triangle)

            # Dessiner la roue arrière
            pygame.draw.circle(self.screen, self.couleurs[3], (int(points_triangle[0][0]), int(points_triangle[0][1])), 3)

            # Dessiner les roues avant (ovales) 
            largeur_roue = 10  # Largeur de l'ellipse
            hauteur_roue = 5  # Hauteur de l'ellipse
        
            for roue in [points_triangle[1],points_triangle[2]]:
                x, y = roue
               # rect = pygame.Rect(x - largeur_roue // 2, y - hauteur_roue // 2, largeur_roue, hauteur_roue)

                # Appliquer l'orientation globale (vehicule.angle) + l'angle des roues (vehicule.angle_braquage)
                rotation_totale = environnement.vehicule.angle
                surface_roue = pygame.Surface((largeur_roue, hauteur_roue), pygame.SRCALPHA)
                pygame.draw.ellipse(surface_roue, self.couleurs[3], (0, 0, largeur_roue, hauteur_roue))

                # Appliquer la rotation
                surface_roue = pygame.transform.rotate(surface_roue, -rotation_totale)
                rect = surface_roue.get_rect(center=(x, y))
                self.screen.blit(surface_roue, rect.topleft)

                self.dessiner_camera(environnement.vehicule)


            # Afficher les objets (obstacles)
            for obj in objects:
                if len(obj)==4:
                    pygame.draw.polygon(self.screen, self.couleurs[1], obj)
                if len(obj)==2:
                    pygame.draw.circle(self.screen, (150, 0, 150), obj[0], obj[1])
            # Si le traçage est activé, on ajoute un point à la trace
            if environnement.trace_active:
                environnement.tracer_ligne()
            
            # Dessiner la ligne seulement s'il y a au moins deux points
            if len(environnement.traces) > 1:
                pygame.draw.lines(self.screen, (200, 0, 200), False, environnement.traces, 2)

            if environnement.asuivre_act :
                environnement.bouger_cible()  # Déplacer la cible aléatoirement
                pygame.draw.circle(self.screen, self.couleurs[1], (environnement.asuivre[0][0], environnement.asuivre[0][1]), 10)

            # Afficher la vitesse du véhicule à l'écran
            font = pygame.font.SysFont(None, 36)
            vitesse_text = font.render(f"Vitesse: {echelle(abs((abs(environnement.vehicule.vit_Rd)+abs(environnement.vehicule.vit_Rg))/2))} m/s", True, self.couleurs[1])
            self.screen.blit(vitesse_text, (10, 10))
            distance = font.render(f"Distance:{echelle(environnement.vehicule.get_distance())} m", True, self.couleurs[1])
            self.screen.blit(distance, (10, 40))
            vitesse = font.render(f"vitesse droite = {echelle(environnement.vehicule.vit_Rd)}, vitesse gauche {echelle(environnement.vehicule.vit_Rg)}", True, self.couleurs[1])
            self.screen.blit(vitesse, (10, 770))
            pygame.display.flip() # Met à jour l'écran

   
    def dessiner_camera(self, vehicule):
        """
        Affiche un petit rectangle sur le véhicule qui représente la caméra.
        Ce rectangle est tourné selon vehicule.angle_servo.
        """
        # Dimensions du rectangle de la caméra
        camera_width = 10
        camera_height = 5
        camera_color = (150, 60, 150)  # Magenta

        # Créer une surface pour la caméra (avec transparence)
        camera_surface = pygame.Surface((camera_width, camera_height), pygame.SRCALPHA)
        camera_surface.fill(camera_color)

        # Calculer l'angle global de la caméra : angle du véhicule + angle du servo
        global_angle = vehicule.angle + vehicule.angle_servo
        rotated_camera = pygame.transform.rotate(camera_surface, -global_angle)

        # Positionner la caméra à l'avant du véhicule.
        # On calcule l'offset en utilisant l'angle global
        angle_rad = m.radians(global_angle)
        offset_x = m.cos(angle_rad)
        offset_y = m.sin(angle_rad)

        # Calcul de la position finale pour centrer le rectangle tourné
        pos_x = int(vehicule.p_centre[0] + offset_x - rotated_camera.get_width() / 2)
        pos_y = int(vehicule.p_centre[1] + offset_y - rotated_camera.get_height() / 2)

        self.screen.blit(rotated_camera, (pos_x, pos_y))

