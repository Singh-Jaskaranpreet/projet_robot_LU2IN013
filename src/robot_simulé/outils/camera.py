import math
import pygame

class CameraView:
    def __init__(self, environnement, adaptateur, width, height, renderer=None):
        self.environnement = environnement
        self.adaptateur = adaptateur 
        self.width = width
        self.height = height
        self.fov = math.radians(180)  # Champ de vision de 60°
        self.num_rays = width        # Un rayon par colonne
        self.max_distance = 1000     # Distance maximale
        self.renderer = renderer


    def cast_rays(self):
        pos = self.environnement.vehicule.p_centre
        angle = math.radians(self.environnement.vehicule.angle + self.environnement.vehicule.angle_servo)
        start_angle = angle - self.fov / 2
        ray_angle_step = self.fov / self.num_rays

        distances = []
        for ray in range(self.num_rays):
            if not pygame.get_init():  # Vérifie si Pygame est toujours actif
                return distances

            ray_angle = start_angle + ray * ray_angle_step
            distances.append(self.cast_single_ray(pos, ray_angle))
        return distances