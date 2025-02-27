from direct.showbase.ShowBase import ShowBase
from panda3d.core import (
    WindowProperties, 
    CollisionNode, CollisionBox, 
    CollisionTraverser, CollisionHandlerPusher,
    NodePath, LineSegs, 
    Point3, Vec4
)

# On importe l'environnement et la classe Vehicule
from src.modele import Vehicule
from ..modele.environnement3d import Environnement3D

class Affichage3D(ShowBase):
    """
    Classe principale qui hérite de ShowBase (Panda3D) et
    qui gère l'affichage, la caméra, le sol, la création 
    des obstacles et du véhicule en 3D, ainsi que la boucle principale.
    """
    def __init__(self):
        pass