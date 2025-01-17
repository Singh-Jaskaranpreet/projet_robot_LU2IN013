import pygame

# Classe Véhicule
class Vehicule:

    def __init__(self, nom, x, y, vitesse, nb_roues):
        self.nom = nom
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.nb_roues = nb_roues
        self.starting_point_x=x
        self.starting_point_y=y

    
    def acceleration(self, acc):
        self.vitesse += acc

    def deceleration(self, red):
        self.vitesse = max(0, self.vitesse - red)

    def arret(self):
        self.vitesse = 0

    def bouger(self):
        self.x += self.vitesse
    
    def restart(self):
        self.x=self.starting_point_x
        self.vitesse=0

    def gerer_controles(self, keys):
        if keys[pygame.K_RIGHT]:
            self.acceleration(0.5)
        if keys[pygame.K_LEFT]:
            self.deceleration(0.5)
        if keys[pygame.K_SPACE]:
            self.arret()
        if keys[pygame.K_r]:
            self.restart()

