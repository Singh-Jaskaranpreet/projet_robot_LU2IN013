# Classe Véhicule
class Vehicule:

    def __init__(self, nom, x, y, vitesse, nb_roues):
        self.nom = nom
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.nb_roues = nb_roues

    def acceleration(self, acc):
        self.vitesse += acc

    def deceleration(self, red):
        self.vitesse = max(0, self.vitesse - red)

    def arret(self):
        self.vitesse = 0

    def bouger(self):
        self.x += self.vitesse
