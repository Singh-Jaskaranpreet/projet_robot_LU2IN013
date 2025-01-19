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

    def bouger_x(self):
        self.x += self.vitesse
    #ici on diminue y pour monter car dans pygame l'origine se trouve en haut à gauche et y augmente vers le bas
    def bouger_y(self):
        self.y -= self.vitesse
    
    def restart(self):
        self.x=self.starting_point_x
        self.y=self.starting_point_y
        self.vitesse=0

    def gerer_controles(self, keys):
    #ici dir est utilisé pour mémoriser la direction(dernière touche appuyée)
        global dir
        if keys[pygame.K_RIGHT]:
            self.acceleration(0.5)
            dir=1
        elif keys[pygame.K_UP]:
            self.acceleration(0.5)
            dir=2
        elif keys[pygame.K_LEFT]:
            dir=0
        elif keys[pygame.K_DOWN]:
            dir=0
        elif keys[pygame.K_SPACE]:
            self.arret()
            dir=-1
        elif keys[pygame.K_r]:
            self.restart()
            dir=-1
        return dir

