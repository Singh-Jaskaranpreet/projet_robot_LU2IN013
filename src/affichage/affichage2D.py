import pygame
import math as m
import config

# Initialisation de Pygame
pygame.init()

def echelle(x):
    return round(config.VITESSE_ECHELLE * x, 3)

class Affichage2D:
    # Dimensions de la fenêtre
    def __init__(self, largeur=config.LARGEUR, hauteur=config.HAUTEUR):
        self.largeur = largeur
        self.hauteur = hauteur
        self.screen = pygame.display.set_mode((largeur, hauteur))
        self.couleurs = config.COULEURS  # Utilisation des couleurs définies dans config

    def afficher(self, objects, environnement):
        pygame.display.set_caption("Simulation de Véhicule")
        self.screen.fill(self.couleurs[0])  # Remplir l'écran en blanc

        # Afficher le véhicule sous forme de triangle
        points_triangle = environnement.vehicule.position_des_roues(environnement.vehicule.p_centre)
        pygame.draw.polygon(self.screen, self.couleurs[2], points_triangle)

        # Dessiner la roue arrière
        pygame.draw.circle(self.screen, self.couleurs[3], (int(points_triangle[0][0]), int(points_triangle[0][1])), 3)

        # Dessiner les roues avant (ovales) avec les valeurs provenant de config.py
        for roue in [points_triangle[1], points_triangle[2]]:
            x, y = roue
            rotation_totale = environnement.vehicule.angle
            surface_roue = pygame.Surface((config.LARGEUR_ROUE, config.HAUTEUR_ROUE), pygame.SRCALPHA)
            pygame.draw.ellipse(surface_roue, self.couleurs[3], (0, 0, config.LARGEUR_ROUE, config.HAUTEUR_ROUE))

            # Appliquer la rotation
            surface_roue = pygame.transform.rotate(surface_roue, -rotation_totale)
            rect = surface_roue.get_rect(center=(x, y))
            self.screen.blit(surface_roue, rect.topleft)

        self.dessiner_camera(environnement.vehicule)

        # Afficher les objets (obstacles)
        for obj in objects:
            if len(obj) == 4:
                pygame.draw.polygon(self.screen, self.couleurs[1], obj)
            if len(obj) == 2:
                pygame.draw.circle(self.screen, (150, 0, 150), obj[0], obj[1])

        # Si le traçage est activé, on ajoute un point à la trace
        if environnement.trace_active:
            environnement.tracer_ligne()

        # Dessiner la ligne seulement s'il y a au moins deux points
        if len(environnement.traces) > 1:
            pygame.draw.lines(self.screen, (200, 0, 200), False, environnement.traces, 2)

        if environnement.asuivre_act:
            environnement.bouger_cible()  # Déplacer la cible aléatoirement
            pygame.draw.circle(self.screen, self.couleurs[1], (environnement.asuivre[0][0], environnement.asuivre[0][1]), 10)

        # Afficher la vitesse du véhicule à l'écran
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {echelle(abs((abs(environnement.vehicule.vit_Rd) + abs(environnement.vehicule.vit_Rg)) / 2))} m/s", True, self.couleurs[1])
        self.screen.blit(vitesse_text, (10, 10))
        distance = font.render(f"Distance:{echelle(environnement.vehicule.get_distance())} m", True, self.couleurs[1])
        self.screen.blit(distance, (10, 40))
        vitesse = font.render(f"vitesse droite = {echelle(environnement.vehicule.vit_Rd)}, vitesse gauche {echelle(environnement.vehicule.vit_Rg)}", True, self.couleurs[1])
        self.screen.blit(vitesse, (10, 770))
        pygame.display.flip()  # Met à jour l'écran

    def dessiner_camera(self, vehicule):
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