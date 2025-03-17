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