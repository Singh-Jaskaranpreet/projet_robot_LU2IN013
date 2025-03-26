from ursina import *
import config


class Affichage3D():
    def __init__(self, environnement):
        self.app = Ursina()  # Initialisation de Ursina
        self.environnement = environnement
        self.voiture = environnement.vehicule
        self.v_G = self.voiture.vit_Rg
        self.v_D = self.voiture.vit_Rd
        self.trace = []
        self.ActiveTrace = False

        # Création du sol
        ground = Entity(
            model='plane', 
            scale=(self.environnement.hauteur, 1, self.environnement.largeur),
            color=config.COULEURS_3D['sol'],  # Utilisation de la couleur du sol
            collider='box',
            position=(self.environnement.hauteur / 2, 0, self.environnement.largeur / 2),
        )

        mur_face = Entity(
            model='cube',
            scale=(self.environnement.hauteur, config.TAILLE_MUR, 0),
            color=config.COULEURS_3D['mur'],
            collider='box',
            world_position=(self.environnement.hauteur / 2, 0, self.environnement.largeur)
        )

        mur_gauche = Entity(
            model='cube',
            scale=(0, config.TAILLE_MUR, self.environnement.largeur),
            color=config.COULEURS_3D['mur'],
            collider='box',
            world_position=(self.environnement.hauteur, 0, self.environnement.largeur/2)
        )

        mur_droite = Entity(
            model='cube',
            scale=(0, config.TAILLE_MUR, self.environnement.largeur),
            color=config.COULEURS_3D['mur'],
            collider='box',
            world_position=(0, 0, self.environnement.largeur/2)            
        )

        mur_der = Entity(
            model='cube',
            scale=(self.environnement.hauteur, config.TAILLE_MUR, 0),
            color=config.COULEURS_3D['mur'],
            collider='box',
            world_position=(self.environnement.hauteur / 2, 0, 0)        
        )

        

        # Création du véhicule 3D
        self.vehicule_3d = self.creer_vehicule3D()

        # Création et récupération des obstacles 3D
        self.objets_3d = []
        self.generer_obstacles()

        # Position initiale de la caméra
        camera.position = config.CAMERA_POSITION  # Utiliser la position définie dans config.py
        camera.look_at(self.vehicule_3d)  # Faire en sorte que la caméra regarde le véhicule
        #camera.parent = self.vehicule_3d

    def creer_vehicule3D(self):
        vehicule_3d = Entity(
            model=Mesh(vertices=[

                # Base (triangle isocèle)
                Vec3(0, 1, -self.voiture.long),  # Point 0 (roue arrière)
                Vec3(-self.voiture.essieux // 2, 1, 0),  # Point 1 (roue gauche)
                Vec3(self.voiture.essieux // 2, 1, 0),  # Point 2 (roue droite)
            ],
            # Base inférieure (permet de relier les 3 points)
            triangles=[(2, 1, 0)]),
            
            color=config.COULEURS_3D['vehicule'],  # Utiliser la couleur du véhicule
        )

        # Roues du véhicule (en bas du prisme triangulaire)
        roue_G = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(-self.voiture.essieux // 2, 1, 0), 
            color=config.COULEURS_3D['roue'], 
            parent=vehicule_3d
        )
        roue_D = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(self.voiture.essieux // 2, 1, 0), 
            color=config.COULEURS_3D['roue'], 
            parent=vehicule_3d
        )
        roue_Ar = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(0, 1, -self.voiture.long), 
            color=config.COULEURS_3D['roue'], 
            parent=vehicule_3d
        )

        vehicule_3d.position = (self.voiture.p_centre[1], 1, self.voiture.p_centre[0])
    
        return vehicule_3d
    def Tracer(self,position):
        """Permet de Creer l'entiter qui va être considérer comme un trait"""
        #Creation du Trait
        new_trace_point = Entity(
                model='cube',
                scale=(0.8, 0.8, 0.8),  # Cube plat
                position=position,  # Position ajustée
                color=color.black
            )

    def generer_obstacles(self):
        """Générer dynamiquement les obstacles 3D à partir de l'environnement."""
        for obj in self.environnement.objects:
            if len(obj) == 4:  # Obstacle rectangulaire
                pos_x = (obj[0][0] + obj[2][0]) / 2
                pos_y = 0
                pos_z = (obj[0][1] + obj[2][1]) / 2
                scale_z = abs(obj[0][0] - obj[2][0])
                scale_x = abs(obj[0][1] - obj[2][1])
                obstacle = Entity(
                    model='cube', 
                    scale=(scale_x, 10, scale_z), 
                    position=(pos_z, pos_y, pos_x), 
                    color=config.COULEURS_3D['obstacle_rect'], 
                    collider='box'
                )
                self.objets_3d.append(obstacle)
            elif len(obj) == 2:  # Obstacle circulaire
                pos_x, pos_z = obj[0]
                rayon = obj[1]
                obstacle = Entity(
                    model='sphere', 
                    scale=(rayon, rayon, rayon), 
                    position=(pos_x, 0.5, pos_z), 
                    color=config.COULEURS_3D['obstacle_circulaire'], 
                    collider='sphere'
                )
                self.objets_3d.append(obstacle)