import random
from src.modele.vehicule import Vehicule
from src.modele.horloge import Horloge
from src.modele.obstacle import Obstacle

from direct.interval.IntervalGlobal import Sequence, Func
from direct.task import Task
from panda3d.core import Point3

class Environnement3D:
    """
    Gère la logique globale de l'environnement : 
    - la liste des véhicules,
    - la liste des obstacles,
    - le déplacement aléatoire via Sequence,
    - la mise à jour (collisions, etc.).
    """
    def __init__(self, showbase):
        # showbase = instance de ShowBase pour accéder à taskMgr, etc.
        self.showbase = showbase
        
        self.vehicules = []
        self.obstacles = []

        # On crée un obstacle unique
        # Exemple : 10 cm x 40 cm x 50 cm -> 0.1 x 0.4 x 0.5 en Panda3D (selon l'echelle)
        # Positionné (0,0,0) => le coin bas/centre
        obstacle = Obstacle(pos=Point3(0, 0, 0),
                            width=0.1, 
                            length=0.4, 
                            height=0.5)
        self.obstacles.append(obstacle)