import random
from .vehicule import Vehicule
from .horloge import Horloge

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
