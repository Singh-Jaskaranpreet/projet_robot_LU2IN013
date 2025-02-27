from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    WindowProperties, 
    CollisionNode, CollisionBox, 
    CollisionTraverser, CollisionHandlerPusher,
    NodePath, LineSegs, 
    Point3, Vec4
)
from panda3d.core import CardMaker, NodePath

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
        cm = CardMaker('floor')
        cm.setFrame(-50, 50, -50, 50)  # définit la taille du plan
        floor = NodePath(cm.generate())
        floor.reparentTo(self.render)
        floor.setP(-90)  # orienter le plan horizontalement
        floor.setColor(1, 1, 1, 1)  # couleur blanche  # Plane par défaut
        floor.setScale(100, 100, 1)       # Un grand sol
        floor.setPos(0, 0, 0)
        floor.setColor(1, 1, 1, 1)        # Blanc
        floor.reparentTo(self.render)

        # 2/ Création de l'obstacle (noir)
        # On prend un modèle "box" de base pour illustrer
        obstacleModel = self.loader.loadModel("models/box")
        # L'obstacle de l'environnement fait 0.1 × 0.4 × 0.5 (largeur, longueur, hauteur)
        # Pour le visuel, on applique un setScale(x, y, z)
        obstacleModel.setScale(1, 4, 5)
        # On le met au sol, la hauteur 0.5 => la moitié doit être au-dessus du sol
        obstacleModel.setPos(0, 0, 0.25)
        obstacleModel.setColor(0, 0, 0, 1)  # Noir
        obstacleModel.reparentTo(self.render)

        # 3/ Création du véhicule
        # Exemple d'instance de la classe Véhicule
        self.vehicule = Vehicule(nom="RobotTest", p_centre=[0, -20], empattement=30, essieux=[10, 20], environnement=self.environnement)

        # On crée un NodePath (3D) pour représenter visuellement le véhicule
        self.vehiculeNP = self.loader.loadModel("models/box")
        # Échelle 0.3 × 0.2 × 0.2 => ~30cm × 20cm × 20cm
        self.vehiculeNP.setScale(3, 2, 2)
        # Couleur (rouge ici, mais vous pouvez la faire varier)
        self.vehiculeNP.setColor(1, 0, 0, 1)
        # On attache le NodePath à la scène
        self.vehiculeNP.reparentTo(self.render)
        # On le place un peu en arrière sur la scène
        self.vehiculeNP.setPos(0, 0, 0.1)




        # 4/ Ajout des roues visibles
        # Pour simplifier, on utilise un cylindre (models/cylinder) pour chaque roue.
        # Deux roues devant :
        wheel1 = self.loader.loadModel("models/misc/rgbCube")
        wheel1.setScale(0.05, 0.05, 0.02)  # Diamètre ~5cm, épaisseur 2cm
        wheel1.setColor(0, 0, 1, 1)       # Bleu
        wheel1.setPos(0.1, 0.1, -0.05)    # Sous le châssis
        wheel1.reparentTo(self.vehiculeNP)

        wheel2 = self.loader.loadModel("models/misc/rgbCube")
        wheel2.setScale(0.05, 0.05, 0.02)
        wheel2.setColor(0, 0, 1, 1)
        wheel2.setPos(-0.1, 0.1, -0.05)
        wheel2.reparentTo(self.vehiculeNP)

        # Stabilisateur arrière (petit cube par exemple)
        stabilisateur = self.loader.loadModel("models/misc/rgbCube")
        stabilisateur.setScale(0.02, 0.02, 0.02)
        stabilisateur.setColor(0, 1, 0, 1)  # Vert
        stabilisateur.setPos(0, -0.1, -0.05)
        stabilisateur.reparentTo(self.vehiculeNP)

        self.vehiculeNP.setPythonTag("speed", 5.0)  # Vitesse en unités/sec


        # 5/ Lancement du mouvement aléatoire
        self.environnement.newDestinations(self.vehiculeNP)

        # 6/ Gestion des tâches
        # On ajoute la tâche d'update de l'environnement
        self.taskMgr.add(self.environnement.update, "UpdateTask")

        # 7/ Position de la caméra
        self.cam.setPos(0, -60, 30)
        self.cam.lookAt(0, 0, 0)

        # 8/ Système de collisions
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # --- Collision pour le véhicule ---
        vehiculeColliderNode = CollisionNode('vehicule_cnode')
        # On crée une "box" centrée sur (0,0,0.1) avec demi-dimensions (0.15, 0.1, 0.1)
        vehiculeColliderNode.addSolid(CollisionBox(Point3(0, 0, 0.1), 0.15, 0.1, 0.1))
        vehiculeCollider = self.vehiculeNP.attachNewNode(vehiculeColliderNode)
        # Le pusher va repousser le véhicule s'il touche un obstacle
        self.pusher.addCollider(vehiculeCollider, self.vehiculeNP)
        self.cTrav.addCollider(vehiculeCollider, self.pusher)

        # --- Collision pour l'obstacle ---
        obstacleColliderNode = CollisionNode('obstacle_cnode')
        # Boîte centrée sur (0,0,0.25) avec demi-dimensions (0.05, 0.2, 0.25)
        obstacleColliderNode.addSolid(CollisionBox(Point3(0, 0, 0.25), 0.05, 0.2, 0.25))
        obstacleCollider = obstacleModel.attachNewNode(obstacleColliderNode)
        # On "repousse" l'obstacle s'il y a collision (ou on peut le laisser fixe)
        # En général, pour un obstacle fixe, on ne l'associe pas au pusher, 
        # mais on peut le faire si on veut qu'il soit statique.
        self.pusher.addCollider(obstacleCollider, obstacleModel)
        self.cTrav.addCollider(obstacleCollider, self.pusher)

        # 9/ Visualisation du vecteur de direction
        # Pour l'exemple, on dessine une ligne depuis le centre du véhicule
        # vers l'avant (Z positif dans ce setup).
        ls = LineSegs()
        ls.setColor(1, 0, 0, 1)
        ls.moveTo(0, 0, 0)
        ls.drawTo(0, 0, 1.0)  # 1 mètre vers l'avant
        directionNP = self.vehiculeNP.attachNewNode(ls.create())

        # 10/ Lancement de l'application
        # (dans un script Panda3D, on termine par run() )


# Point d'entrée si on exécute ce fichier directement
if __name__ == "__main__":
    app = Affichage3D()
    app.run()