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

    def tourner_gauche(self, environnement, objects):
        """
        Tente de tourner à gauche, en vérifiant d'abord les collisions potentielles.
        """
        nouvel_angle = self.angle - 1
        tmp = (nouvel_angle / 180) * m.pi

        # Précalcul des positions après rotation
        nouveau_r_Avg = [
            self.r_Ar[0] + self.long * m.cos(((nouvel_angle + 20) / 180) * m.pi),
            self.r_Ar[1] + self.long * m.sin(((nouvel_angle + 20) / 180) * m.pi),
            ]
        nouveau_r_Avd = [
            self.r_Ar[0] + self.long * m.cos(((nouvel_angle - 20) / 180) * m.pi),
            self.r_Ar[1] + self.long * m.sin(((nouvel_angle - 20) / 180) * m.pi),
            ]

        # Tester la collision
        if not environnement.collision_pre_rotation([self.r_Ar, nouveau_r_Avg, nouveau_r_Avd], objects):
            # Appliquer la rotation si elle est valide
            self.angle = nouvel_angle
            self.direction_x = m.cos(tmp)
            self.direction_y = m.sin(tmp)
            self.r_Avg = nouveau_r_Avg
            self.r_Avd = nouveau_r_Avd
        else:
            print("oh là là, où tu crois tourner")
            
    def tourner_droite(self, environnement, objects):
        """
        Tente de tourner à droite, en vérifiant d'abord les collisions potentielles.
        """
        nouvel_angle = self.angle + 1
        tmp = (nouvel_angle / 180) * m.pi

        # Précalcul des positions après rotation
        nouveau_r_Avg = [
            self.r_Ar[0] + self.long * m.cos(((nouvel_angle + 20) / 180) * m.pi),
            self.r_Ar[1] + self.long * m.sin(((nouvel_angle + 20) / 180) * m.pi),
            ]
        nouveau_r_Avd = [
            self.r_Ar[0] + self.long * m.cos(((nouvel_angle - 20) / 180) * m.pi),
            self.r_Ar[1] + self.long * m.sin(((nouvel_angle - 20) / 180) * m.pi),
            ]

        # Tester la collision
        if not environnement.collision_pre_rotation([self.r_Ar, nouveau_r_Avg, nouveau_r_Avd], objects):
            # Appliquer la rotation si elle est valide
            self.angle = nouvel_angle
            self.direction_x = m.cos(tmp)
            self.direction_y = m.sin(tmp)
            self.r_Avg = nouveau_r_Avg
            self.r_Avd = nouveau_r_Avd
        else:
            print("oh là là, où tu crois tourner")

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
