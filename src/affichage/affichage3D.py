from ursina import *
import config


class Affichage3D():
    def __init__(self, environnement, controleur):
        self.app = Ursina()  # Initialisation de Ursina
        self.environnement = environnement
        self.voiture = environnement.vehicule
        self.v_G = self.voiture.vit_Rg
        self.v_D = self.voiture.vit_Rd
        self.controleur = controleur

        # Création du sol
        ground = Entity(
            model='plane', 
            scale=(self.environnement.largeur, 1, self.environnement.hauteur),
            color=config.COULEURS['sol'],  # Utilisation de la couleur du sol
            collider='box',
            position=(self.environnement.largeur / 2, 0, self.environnement.hauteur / 2)
        )

        # Création du véhicule 3D
        self.vehicule_3d = self.creer_vehicule3D()

        # Création et récupération des obstacles 3D
        self.objets_3d = []
        self.generer_obstacles()

        # Position initiale de la caméra
        camera.position = config.CAMERA_POSITION  # Utiliser la position définie dans config.py
        camera.look_at(self.vehicule_3d)  # Faire en sorte que la caméra regarde le véhicule

    def creer_vehicule3D(self):
        vehicule_3d = Entity(
            model=Mesh(vertices=[

                # Base (triangle isocèle)
                Vec3(0, 0.1, -config.ESSIEUX / 2),  # Point 0 (roue arrière)
                Vec3(-config.ESSIEUX / 2, 0.1, config.ESSIEUX / 2),  # Point 1 (roue gauche)
                Vec3(config.ESSIEUX / 2, 0.1, config.ESSIEUX / 2),  # Point 2 (roue droite)
            ],
            # Base inférieure (permet de relier les 3 points)
            triangles=[(2, 1, 0)]),
            
            color=config.COULEURS['vehicule'],  # Utiliser la couleur du véhicule
            position=(0, 0.1, 0)
        )

        vehicule_3d.world_position = (self.voiture.p_centre[0], 1, self.voiture.p_centre[1])

        # Roues du véhicule (en bas du prisme triangulaire)
        roue_G = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(-config.ESSIEUX / 2, 0.1, config.ESSIEUX / 2), 
            color=config.COULEURS['roue'], 
            parent=vehicule_3d
        )
        roue_D = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(config.ESSIEUX / 2, 0.1, config.ESSIEUX / 2), 
            color=config.COULEURS['roue'], 
            parent=vehicule_3d
        )
        roue_Ar = Entity(
            model='sphere', 
            scale=config.TAILLE_ROUE, 
            position=(0, 0.1, -config.ESSIEUX / 2), 
            color=config.COULEURS['roue'], 
            parent=vehicule_3d
        )

        return vehicule_3d

    def update(self):
        """
        Affiche l'environnement, y compris le véhicule, les objets (obstacles),
        et la vitesse du véhicule.
        """
        self.controleur.gerer_evenements()
        self.environnement.bouger()
        self.environnement.rester_dans_limites()
        self.vehicule_3d.position = (self.voiture.p_centre[0], 0, self.voiture.p_centre[1])
        self.vehicule_3d.rotation_y = self.voiture.angle

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
                    scale=(scale_x, 2, scale_z), 
                    position=(pos_x, pos_y, pos_z), 
                    color=config.COULEURS['obstacle_rect'], 
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
                    color=config.COULEURS['obstacle_circulaire'], 
                    collider='sphere'
                )
                self.objets_3d.append(obstacle)