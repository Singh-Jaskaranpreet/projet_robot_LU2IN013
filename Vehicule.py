import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, x, y, vitesse, nb_roues):
        self.nom = nom
        self.x = x
        self.y = y
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse = vitesse
        self.nb_roues = nb_roues
        self.starting_point_x=x
        self.starting_point_y=y

    
    def acceleration(self, acc):
        self.vitesse += acc

    def deceleration(self, red):
        self.vitesse = self.vitesse - red

    def arret(self):
        self.vitesse = 0

    def bouger_x(self):
        self.x += self.vitesse*self.direction_x
    #ici on diminue y pour monter car dans pygame l'origine se trouve en haut à gauche et y augmente vers le bas
    def bouger_y(self):
        self.y -= self.vitesse*self.direction_y

    def tourner_gauche(self):
        self.angle = self.angle + 1
        tmp = (self.angle/180)*m.pi
        self.direction_x= m.cos(tmp)
        self.direction_y= m.sin(tmp)

    def tourner_droite(self):
        self.angle = self.angle - 1
        tmp = (self.angle/180)*m.pi
        self.direction_x= m.cos(tmp)
        self.direction_y= m.sin(tmp)

    def restart(self):
        self.x=self.starting_point_x
        self.y=self.starting_point_y
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse=0

    def gerer_controles(self, keys):
    #ici dir est utilisé pour mémoriser la direction(dernière touche appuyée)
    
        if keys[pygame.K_RIGHT]:
            self.tourner_droite()
            
        elif keys[pygame.K_UP]:
            self.acceleration(0.2)
            
        elif keys[pygame.K_LEFT]:
            self.tourner_gauche()
            
        elif keys[pygame.K_DOWN]:
            self.deceleration(0.2)
            
        elif keys[pygame.K_SPACE]:
            self.arret()
            
        elif keys[pygame.K_r]:
            self.restart()
            
        if self.vitesse != 0 :
            self.bouger_x()
            self.bouger_y()


