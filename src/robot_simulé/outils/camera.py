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
    
    def cast_single_ray(self, pos, ray_angle):
        x, y = pos
        for d in range(0, self.max_distance, 5):
            test_x = x + d * math.cos(ray_angle)
            test_y = y + d * math.sin(ray_angle)
            
            for obj in self.environnement.objects:
                if len(obj) == 4:  # 🔴 Cas des rectangles
                    if (obj[0][0] <= test_x <= obj[2][0]) and (obj[0][1] <= test_y <= obj[2][1]):
                        return d

                elif len(obj) == 2:  # 🔵 Cas des cercles
                    cx, cy = obj[0]  # Centre du cercle
                    rayon = obj[1]   # Rayon du cercle
                    
                    distance_objet = math.sqrt((test_x - cx) ** 2 + (test_y - cy) ** 2)
                    if distance_objet <= rayon:
                        return d  # Distance de détection du cercle

            if test_x < 0 or test_x > self.environnement.largeur or test_y < 0 or test_y > self.environnement.hauteur:
                return d

        return self.max_distance