import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse, p_centre ,longueur, nb_roues):
        self.nom = nom
        self.long=longueur # Distance entre les essieux
        self.angle = 0
        self.p_centre = p_centre
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse = vitesse
        self.starting_point_x=p_centre[0]
        self.starting_point_y=p_centre[1]
        self.angle_braquage = 0  # Angle des roues avant (en degrés)
        self.nb_roues = nb_roues

    #Place les trois roues de la voiture
    def position_des_roues(self,point):
        hyp = self.long / m.cos(m.radians(20))
        r_Ar = [point[0]-(self.long//2)*m.cos(m.radians(self.angle)),point[1]-(self.long//2)*m.sin(m.radians(self.angle)) ]
        r_Avg = [r_Ar[0] + hyp * m.cos(m.radians(self.angle + 20)),r_Ar[1] + hyp * m.sin(m.radians(self.angle + 20))]
        r_Avd = [r_Ar[0] + hyp * m.cos(m.radians(self.angle - 20)),r_Ar[1] + hyp * m.sin(m.radians(self.angle - 20))]
        return [r_Ar,r_Avg,r_Avd]
     

    def acceleration(self, acc):
        self.vitesse = min(self.vitesse + acc , 7.5)

    def deceleration(self, red):
        self.vitesse = max(self.vitesse - red , -7.5)

    def arret(self):
        self.vitesse = 0

    def bouger(self, environnement, objects):
        """Déplace le véhicule en fonction de l'orientation, du braquage et des collisions."""
        if self.angle_braquage != 0 and self.vitesse != 0:
            # Rayon de courbure en fonction de l'angle de braquage
            rayon_courbure = self.long / m.tan(m.radians(self.angle_braquage))
            delta_angle = self.vitesse / rayon_courbure
            self.angle += m.degrees(delta_angle)


        # Calculer les nouvelles coordonnées sans encore les appliquer
        prochain_pos = [
            self.p_centre[0] + self.vitesse * m.cos(m.radians(self.angle)),
            self.p_centre[1] + self.vitesse * m.sin(m.radians(self.angle))
        ]
        
        if environnement.collision_predeplacement(self, objects):
            self.vitesse = 0  # Arrête le véhicule en cas de collision
            return

        # Appliquer les nouvelles coordonnées si aucune collision
        self.p_centre = prochain_pos

    def tourner(self, direction):
        """ Gère le braquage des roues en fonction de la direction. """
        if direction == "gauche":
            self.braquer(-1.5)
        elif direction == "droite":
            self.braquer(1.5)

    def restart(self):
        self.p_centre=[self.starting_point_x,self.starting_point_y]
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse=0
        self.angle_braquage = 0


    def bouger_retour(self):
        """
        Recule légèrement pour empêcher le véhicule d'entrer dans un obstacle.
        """
        self.p_centre[0] -= self.vitesse * self.direction_x
        self.p_centre[1] -= self.vitesse * self.direction_y

    def braquer(self, angle):
        """ Modifie l'angle de braquage des roues avant. """
        self.angle_braquage += angle
        self.angle_braquage = max(-45, min(45, self.angle_braquage))  # Limite réaliste
