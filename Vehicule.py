import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse,coord, longueur, nb_roues):
        self.nom = nom
        self.long=longueur # Distance entre les essieux
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse = vitesse
        self.starting_point_x=coord[0]
        self.starting_point_y=coord[1]
        self.angle_braquage = 0  # Angle des roues avant (en degrés)
        self.nb_roues = nb_roues

        # Position des roues arrière
        self.r_Ar = [coord[0], coord[1]]

        # Positions des roues avant avec l'angle initial
        self.r_Avg = [
            self.r_Ar[0] + self.long * m.cos(m.radians(self.angle + 20)),
            self.r_Ar[1] + self.long * m.sin(m.radians(self.angle + 20))
        ]
        self.r_Avd = [
            self.r_Ar[0] + self.long * m.cos(m.radians(self.angle - 20)),
            self.r_Ar[1] + self.long * m.sin(m.radians(self.angle - 20))
        ]

    
    def acceleration(self, acc):
        self.vitesse = min(self.vitesse + acc , 7.5)

    def deceleration(self, red):
        self.vitesse = max(self.vitesse + red , -7.5)

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

    def tourner(self, direction):
        """ Gère le braquage des roues en fonction de la direction. """
        if direction == "gauche":
            self.braquer(-1.5)
        elif direction == "droite":
            self.braquer(1.5)

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


    def bouger_retour(self):
        """
        Recule légèrement pour empêcher le véhicule d'entrer dans un obstacle.
        """
        self.r_Ar[0] -= self.vitesse * self.direction_x
        self.r_Ar[1] -= self.vitesse * self.direction_y
        self.r_Avd[0] -= self.vitesse * self.direction_x
        self.r_Avd[1] -= self.vitesse * self.direction_y
        self.r_Avg[0] -= self.vitesse * self.direction_x
        self.r_Avg[1] -= self.vitesse * self.direction_y

    def braquer(self, angle):
        """ Modifie l'angle de braquage des roues avant. """
        self.angle_braquage += angle
        self.angle_braquage = max(-45, min(45, self.angle_braquage))  # Limite réaliste
