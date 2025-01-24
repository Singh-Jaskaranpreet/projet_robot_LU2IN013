import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse,coord, long):
        self.nom = nom
        self.long=long
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse = vitesse
        self.r_Ar=[coord[0],coord[1]]
        self.r_Avd=[coord[0]+long*m.cos(m.pi/9),coord[1]+long*m.sin(m.pi/9)]
        self.r_Avg=[coord[0]+long*m.cos(m.pi/9),coord[1]-long*m.sin(m.pi/9)]
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
        self.r_Ar[1] += self.vitesse*self.direction_y
        self.r_Avd[1] += self.vitesse*self.direction_y
        self.r_Avg[1] += self.vitesse*self.direction_y

    def tourner_gauche(self):
        self.angle = self.angle - 1
        tmp = (self.angle/180)*m.pi
        self.direction_x= m.cos(tmp)
        self.direction_y= m.sin(tmp)
        self.r_Avg[0]=self.r_Ar[0]+self.long*m.cos(((self.angle+20)/180)*m.pi)
        self.r_Avg[1]=self.r_Ar[1]+self.long*m.sin(((self.angle+20)/180)*m.pi)
        self.r_Avd[0]=self.r_Ar[0]+self.long*m.cos(((self.angle-20)/180)*m.pi)
        self.r_Avd[1]=self.r_Ar[1]+self.long*m.sin(((self.angle-20)/180)*m.pi)

    def tourner_droite(self):
        self.angle = self.angle + 1
        tmp = (self.angle/180)*m.pi
        self.direction_x= m.cos(tmp)
        self.direction_y= m.sin(tmp)
        self.r_Avg[0]=self.r_Ar[0]+self.long*m.cos(((self.angle+20)/180)*m.pi)
        self.r_Avg[1]=self.r_Ar[1]+self.long*m.sin(((self.angle+20)/180)*m.pi)
        self.r_Avd[0]=self.r_Ar[0]+self.long*m.cos(((self.angle-20)/180)*m.pi)
        self.r_Avd[1]=self.r_Ar[1]+self.long*m.sin(((self.angle-20)/180)*m.pi)
        

    def restart(self):
        self.r_Ar=[self.starting_point_x,self.starting_point_y]
        self.r_Avd=[self.starting_point_x+self.long*m.cos(m.pi/9),self.starting_point_y+self.long*m.sin(m.pi/9)]
        self.r_Avg=[self.starting_point_x+self.long*m.cos(m.pi/9),self.starting_point_y-self.long*m.sin(m.pi/9)]
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse=0

    def gerer_controles(self, keys):
    #ici dir est utilisé pour mémoriser la direction(dernière touche appuyée)
        dir = ""

        if keys[pygame.K_RIGHT]:
            #self.tourner_droite()
            dir="droite"

        elif keys[pygame.K_LEFT]:
            #self.tourner_gauche()
            dir="gauche"
            
        elif keys[pygame.K_UP]:
            #self.acceleration(0.2)
            dir="acceleration"        
            
        elif keys[pygame.K_DOWN]:
            #self.deceleration(0.2)
            dir="deceleration"
            
        elif keys[pygame.K_SPACE]:
            #self.arret()
            dir="stop"
            
        elif keys[pygame.K_r]:
            #self.restart()
            dir="restart"
            
        #if self.vitesse != 0 :
            #self.bouger_x()
            #self.bouger_y()

        return dir


