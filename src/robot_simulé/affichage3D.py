from ursina import *
from .environnement import Environnement

# Initialisation de Ursina
app = Ursina()

class Affichage3D:
    def __init__(self):
        pass

    def afficher(self, objects, environnement):
        """
        Affiche l'environnement, y compris le véhicule, les objets (obstacles),
        et la vitesse du véhicule.
        """
        
        # Création du sol                    (x,   y,  z)
        ground = Entity(model='plane', scale=(100, 1, 100), color=color.white, collider='box')


        # Créer la voiture et les roues
        # Création d'un robot en forme de triangles isocèles
       
        robot = Entity(
            model=Mesh(vertices=[

        # Base(triangle isocèle)
            Vec3(0, 0.1, -0.5), # Point 0 (roue arrière)
            Vec3(-0.5, 0.1, 2),  # Point 1 (roue gauche)
            Vec3(0.5, 0.1, 2),   # Point 2 (roue droite)
            
            ], 
        # Base inférieure(permet de relier les 3 points)
            triangles=[(2, 1, 0)]),
            
        color=color.red,  # Remplissage rouge
        position=(0, 0.1, 0)
        )

        # Roues de la voiture (en bas du prisme triangulaire)
        front_left_wheel = Entity(model='sphere', scale=0.2, position=(-0.5, 0.1, 2), color=color.black , parent=robot)                                                                                                                                                                                                                                                   
        front_right_wheel = Entity(model='sphere', scale=0.2, position=(0.5, 0.1, 2), color=color.black , parent= robot)
        back_wheel = Entity(model='sphere', scale=0.2, position=(0, 0.1, -0.5), color=color.black,parent= robot)
