from ursina import *



class Affichage3D:
    def __init__(self,voiture):
        self.app = Ursina() # Initialisation de Ursina
        self.voiture = voiture
        self.v_G = self.voiture.vit_Rg
        self.v_D = self.voiture.vit_Rd

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
        roue_G = Entity(model='sphere', scale=0.2, position=(-0.5, 0.1, 2), color=color.black , parent=robot)                                                                                                                                                                                                                                                   
        roue_D = Entity(model='sphere', scale=0.2, position=(0.5, 0.1, 2), color=color.black , parent= robot)
        roue_Ar = Entity(model='sphere', scale=0.2, position=(0, 0.1, -0.5), color=color.black,parent= robot)

        # Position initiale de la caméra
        camera.position = (0, 5, -12)
        camera.look_at(robot)  # Faire en sorte que la caméra regarde le robot


        self.app.run()