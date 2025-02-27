class Obstacle:
    """
    Représente un obstacle rectangulaire dans l'environnement.
    width, length, height en 'mètres' (ou autre échelle).
    """
    def __init__(self, pos, width, length, height):
        self.pos = pos
        self.width = width
        self.length = length
        self.height = height