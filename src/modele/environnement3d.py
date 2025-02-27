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

    def randomPoint(self):
        """ Génère un point aléatoire dans la scène """
        x = random.uniform(-40, 40)  # Adaptez selon la taille de votre sol
        y = random.uniform(-40, 40)
        z = 0  # On reste au sol
        return Point3(x, y, z)

    def newDestinations(self, s):
        # Définir une nouvelle destination aléatoire
        target = self.randomPoint()
        s.setPythonTag("target", target)

        # Calcul de la durée d'animation
        distance = (s.getPos() - target).length()
        speed = s.getPythonTag("speed")
        dt = distance / speed if speed > 0 else 1.0


        # Création de la séquence d'animation vers la nouvelle cible
        sequence = Sequence(
            s.posInterval(dt, target),
            Func(self.sequenceDone, s)
        )
        s.setPythonTag("sequence", sequence)

        s.lookAt(target)
        sequence.start()

    def sequenceDone(self, s):
        """
        Une fois la séquence terminée, programme une nouvelle destination
        en utilisant doMethodLater pour laisser le temps aux séquences de se terminer.
        """
        self.showbase.taskMgr.doMethodLater(0, self.newDestinations, "nextDestination", extraArgs=[s])

    def update(self, task):
        """
        Méthode d'update appelée par le taskMgr de Panda3D.
        On peut y ajouter la gestion de collisions ou autres mises à jour de la simulation.
        """
        # Par exemple : vérification de collisions, mise à jour des états, etc.
        return Task.cont