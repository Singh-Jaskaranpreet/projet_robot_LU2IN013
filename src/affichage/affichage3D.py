from ursina import *



class Affichage3D:
    def __init__(self,environnement):
        self.app = Ursina() # Initialisation de Ursina
        self.environnement = environnement
        self.voiture = environnement.vehicule
        self.v_G = self.voiture.vit_Rg
        self.v_D = self.voiture.vit_Rd

        # Création du sol                    (x,   y,  z)
        ground = Entity(model='plane', scale=(environnement.largeur, 1, environnement.hauteur), color=color.white, collider='box',position=(environnement.largeur/2,0,environnement.hauteur/2))

        #création du vehicule 3D
        self.vehicule_3d = self.creer_vehicule3D()

        # Création et recupération des obstacles 3D
        self.objets_3d = []
        self.generer_obstacles()
        
    def creer_vehicule3D(self):
        vehicule_3d = Entity(
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
        vehicule_3d.world_position = (self.voiture.p_centre[0],1,self.voiture.p_centre[1])
        # Roues de la voiture (en bas du prisme triangulaire)
        roue_G = Entity(model='sphere', scale=0.2, position=(-0.5, 0.1, 2), color=color.black , parent= vehicule_3d)                                                                                                                                                                                                                                                   
        roue_D = Entity(model='sphere', scale=0.2, position=(0.5, 0.1, 2), color=color.black , parent= vehicule_3d)
        roue_Ar = Entity(model='sphere', scale=0.2, position=(0, 0.1, -0.5), color=color.black,parent= vehicule_3d)
        
        # Pivot de la voiture
        pivot_D = Entity(position = (0.5, 0.1, 2), parent = vehicule_3d )
        pivot_G = Entity(position = (-0.5, 0.1, 2) , parnet = vehicule_3d )
        return vehicule_3d

    def afficher(self):
        """
        Affiche l'environnement, y compris le véhicule, les objets (obstacles),
        et la vitesse du véhicule.
        """

        # Créer la voiture et les roues
        # Création d'un robot en forme de triangles isocèles
        
        # Position initiale de la caméra
        camera.position = (self.voiture.p_centre[0], 5, self.voiture.p_centre[1]-20)
        camera.look_at(self.vehicule_3d)  # Faire en sorte que la caméra regarde le robot
        camera.world_parent = self.vehicule_3d

        #
        self.vehicule_3d.world_position = (self.voiture.p_centre[0],0,self.voiture.p_centre[1])
        self.vehicule_3d.world_rotation_y = self.voiture.angle
        self.app.run()

    def generer_obstacles(self):
        """Générer dynamiquement les obstacles 3D à partir de l'environnement."""
        for obj in self.environnement.objects:
            if len(obj) == 4:  # Obstacle rectangulaire
                pos_x = (obj[0][0] + obj[2][0]) / 2
                pos_y = 0
                pos_z = (obj[0][1] + obj[2][1]) / 2
                scale_z = abs(obj[0][0] - obj[2][0])
                scale_x = abs(obj[0][1] - obj[2][1])
                obstacle = Entity(model='cube', scale=(scale_x, 2, scale_z), position=(pos_x, pos_y, pos_z), color=color.magenta, collider='box')
                self.objets_3d.append(obstacle)
            elif len(obj) == 2:  # Obstacle circulaire
                pos_x, pos_z = obj[0]
                rayon = obj[1]
                obstacle = Entity(model='sphere', scale=(rayon, rayon, rayon), position=(pos_x, 0.5, pos_z), color=color.blue, collider='sphere')
                self.objets_3d.append(obstacle)
