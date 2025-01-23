import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse, r_Avg, r_Avd, r_Ar,coord, long):
        self.nom = nom
        self.long=long
    
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse = vitesse
        self.r_Ar=(coord[0],coord[1])
        self.r_Avd=(coord[0]+long*2,coord[1]-(long//2))
        self.r_Avg=((coord[0]+long*2,coord[1]+(long//2)))
        self.starting_point_x=coord[0]
        self.starting_point_y=coord[1]

    
    def acceleration(self, acc):
        self.vitesse += acc

    def deceleration(self, red):
        self.vitesse = self.vitesse - red

    def arret(self):
        self.vitesse = 0

    def bouger_x(self):
        self.r_Ar[0] += self.vitesse*self.direction_x
        self.r_Avd[0] += self.vitesse*self.direction_x
        self.r_Avg[0] += self.vitesse*self.direction_x
    #ici on diminue y pour monter car dans pygame l'origine se trouve en haut à gauche et y augmente vers le bas
    def bouger_y(self):
        self.r_Ar[1] += self.vitesse*self.direction_x
        self.r_Avd[1] += self.vitesse*self.direction_x
        self.r_Avg[1] += self.vitesse*self.direction_x

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


