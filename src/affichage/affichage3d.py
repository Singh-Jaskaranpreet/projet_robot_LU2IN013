from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    WindowProperties, 
    CollisionNode, CollisionBox, 
    CollisionTraverser, CollisionHandlerPusher,
    NodePath, LineSegs, 
    Point3, Vec4
)

# On importe l'environnement et la classe Vehicule
from ..modele import Vehicule
from src.modele.environnement3d import Environnement3D

class Affichage3D(ShowBase):
    """
    Classe principale qui hérite de ShowBase (Panda3D) et
    qui gère l'affichage, la caméra, le sol, la création 
    des obstacles et du véhicule en 3D, ainsi que la boucle principale.
    """
    def __init__(self):

        super().__init__()

        # Paramètres de la fenêtre
        props = WindowProperties()
        props.setTitle("Simulation 3D Robot")
        self.win.requestProperties(props)

        # Création et initialisation de l'environnement
        self.environnement = Environnement3D(self)

        # 1/ Création du sol (blanc)
        floor = self.loader.loadModel("models/plane")  # Plane par défaut
        floor.setScale(100, 100, 1)       # Un grand sol
        floor.setPos(0, 0, 0)
        floor.setColor(1, 1, 1, 1)        # Blanc
        floor.reparentTo(self.render)

        # 2/ Création de l'obstacle (noir)
        # On prend un modèle "box" de base pour illustrer
        obstacleModel = self.loader.loadModel("models/box")
        # L'obstacle de l'environnement fait 0.1 × 0.4 × 0.5 (largeur, longueur, hauteur)
        # Pour le visuel, on applique un setScale(x, y, z)
        obstacleModel.setScale(0.1, 0.4, 0.5)
        # On le met au sol, la hauteur 0.5 => la moitié doit être au-dessus du sol
        obstacleModel.setPos(0, 0, 0.25)
        obstacleModel.setColor(0, 0, 0, 1)  # Noir
        obstacleModel.reparentTo(self.render)

        # 3/ Création du véhicule
        # Exemple d'instance de la classe Véhicule
        self.vehicule = Vehicule(
            nom="RobotTest", 
            p_centre=[0, -20], 
            empattement=30, 
            essieux=[10, 20], 
            angle=0
        )

        # On crée un NodePath (3D) pour représenter visuellement le véhicule
        self.vehiculeNP = self.loader.loadModel("models/box")
        # Échelle 0.3 × 0.2 × 0.2 => ~30cm × 20cm × 20cm
        self.vehiculeNP.setScale(0.3, 0.2, 0.2)
        # Couleur (rouge ici, mais vous pouvez la faire varier)
        self.vehiculeNP.setColor(1, 0, 0, 1)
        # On attache le NodePath à la scène
        self.vehiculeNP.reparentTo(self.render)
        # On le place un peu en arrière sur la scène
        self.vehiculeNP.setPos(0, 0, 0.1)

        # On stocke une "vitesse" pour le NodePath (utilisée par newDestinations)
        self.vehiculeNP.speed = 5.0

        # 4/ Ajout des roues visibles
        # Pour simplifier, on utilise un cylindre (models/cylinder) pour chaque roue.
        # Deux roues devant :
        wheel1 = self.loader.loadModel("models/cylinder")
        wheel1.setScale(0.05, 0.05, 0.02)  # Diamètre ~5cm, épaisseur 2cm
        wheel1.setColor(0, 0, 1, 1)       # Bleu
        wheel1.setPos(0.1, 0.1, -0.05)    # Sous le châssis
        wheel1.reparentTo(self.vehiculeNP)

        wheel2 = self.loader.loadModel("models/cylinder")
        wheel2.setScale(0.05, 0.05, 0.02)
        wheel2.setColor(0, 0, 1, 1)
        wheel2.setPos(-0.1, 0.1, -0.05)
        wheel2.reparentTo(self.vehiculeNP)

        # Stabilisateur arrière (petit cube par exemple)
        stabilisateur = self.loader.loadModel("models/box")
        stabilisateur.setScale(0.02, 0.02, 0.02)
        stabilisateur.setColor(0, 1, 0, 1)  # Vert
        stabilisateur.setPos(0, -0.1, -0.05)
        stabilisateur.reparentTo(self.vehiculeNP)



# Point d'entrée si on exécute ce fichier directement
if __name__ == "__main__":
    app = Affichage3D()
    app.run()