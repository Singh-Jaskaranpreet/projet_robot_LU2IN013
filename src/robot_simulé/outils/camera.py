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
    
    def render(self):
        distances = self.cast_rays()
        if self.environnement.asuivre_act:
                d = self.afficher_balise()
        if self.renderer:
            # Effacer l'écran avec une couleur blanche (inversion des couleurs)
            self.renderer.draw_color = (255, 255, 255, 255)
            self.renderer.clear()

            # Dessiner chaque rayon comme une colonne de pixels
            for i, distance in enumerate(distances):
                column_height = int(5000 / (distance + 1))  # Hauteur relative à la distance
                column_height = min(self.height, column_height)
                color_intensity = max(0, int(distance / 4))

                # Définition d'un rectangle pour représenter la colonne
                rect = pygame.Rect(i, (self.height - column_height) // 2, 1, column_height)
                
                # Détection spéciale pour les cercles → on applique une distorsion pour créer une forme arrondie
                if distance < self.max_distance and isinstance(distance, tuple):  # Si on a détecté un cercle
                    center_distance = abs(i - self.width // 2)  # Distance par rapport au centre
                    attenuation = max(0.5, 1 - center_distance / self.width)  # Effet d'arrondi
                    color_intensity = int(color_intensity * attenuation)
                

                self.renderer.draw_color = (color_intensity, color_intensity, color_intensity, 255)
                self.renderer.fill_rect(rect)

            if self.environnement.asuivre_act:
                for i, distance in enumerate(d):
                    column_height = int(5000 / (distance + 1))  # Hauteur relative à la distance
                    column_height = min(self.height, column_height)
                    color_intensity = max(0, int(distance / 4))
                    rect2 = pygame.Rect(i, (self.height - column_height) // 2, 1, column_height)
                    if distance < self.max_distance and isinstance(distance, tuple):  # Si on a détecté un cercle
                        center_distance = abs(i - self.width // 2)  # Distance par rapport au centre
                        attenuation = max(0.5, 1 - center_distance / self.width)  # Effet d'arrondi
                        color_intensity = int(color_intensity * attenuation)
                    self.renderer.draw_color = (color_intensity, color_intensity, color_intensity, 255)
                    self.renderer.fill_rect(rect2)

            # Mettre à jour l'affichage
            self.renderer.present()

    def afficher_balise(self):
        pos = self.environnement.vehicule.p_centre
        angle = math.radians(self.environnement.vehicule.angle + self.environnement.vehicule.angle_servo)
        start_angle = angle - self.fov / 2
        ray_angle_step = self.fov / self.num_rays

        distances = []
        for ray in range(self.num_rays):
            if not pygame.get_init():  # Vérifie si Pygame est toujours actif
                return distances

            ray_angle = start_angle + ray * ray_angle_step
            distances.append(self.cast_single_ray_b(pos, ray_angle))
        return distances

    def cast_single_ray_b(self, pos, ray_angle):
        x, y = pos
        for d in range(0, self.max_distance, 5):
            test_x = x + d * math.cos(ray_angle)
            test_y = y + d * math.sin(ray_angle)
            
            for obj in self.environnement.asuivre:
                cx, cy = obj  # Centre du cercle
                rayon = 10   # Rayon du cercle
                    
                distance_objet = math.sqrt((test_x - cx) ** 2 + (test_y - cy) ** 2)
                if distance_objet <= rayon:
                    return d  # Distance de détection du cercle

            if test_x < 0 or test_x > self.environnement.largeur or test_y < 0 or test_y > self.environnement.hauteur:
                return d

        return self.max_distance