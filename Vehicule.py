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
        self.vitesse = max(self.vitesse - red , -7.5)

    def arret(self):
        self.vitesse = 0

    def bouger(self, environnement, objects):
        """Déplace le véhicule en tenant compte des collisions et des limites."""

        # Calcul du prochain déplacement AVANT de l'appliquer
        prochain_r_Ar = [
            self.r_Ar[0] + self.vitesse * m.cos(m.radians(self.angle)),
            self.r_Ar[1] + self.vitesse * m.sin(m.radians(self.angle))
        ]
        prochain_r_Avg = [
            prochain_r_Ar[0] + self.long * m.cos(m.radians(self.angle + 20)),
            prochain_r_Ar[1] + self.long * m.sin(m.radians(self.angle + 20))
        ]
        prochain_r_Avd = [
            prochain_r_Ar[0] + self.long * m.cos(m.radians(self.angle - 20)),
            prochain_r_Ar[1] + self.long * m.sin(m.radians(self.angle - 20))
        ]

        prochain_triangle = [prochain_r_Ar, prochain_r_Avg, prochain_r_Avd]

        # 🚨 Vérification des collisions AVANT déplacement
        if environnement.collision_predeplacement(prochain_triangle, objects):
            self.vitesse = 0
            return

        # 🛑 Vérification spécifique : roue arrière bloquée en reculant
        if self.vitesse < 0 and environnement.collision_roue_arriere(self, objects):
            self.vitesse = 0
            return  # 🚨 Empêche complètement la rotation et le mouvement

        # 📌 Mise à jour des positions SI aucune collision détectée
        self.r_Ar = prochain_r_Ar
        self.r_Avg = prochain_r_Avg
        self.r_Avd = prochain_r_Avd

        # 🔄 Appliquer la rotation UNIQUEMENT si aucune collision détectée
        if self.angle_braquage != 0 and self.vitesse != 0:
            rayon_courbure = self.long / m.tan(m.radians(self.angle_braquage))
            delta_angle = self.vitesse / rayon_courbure
            self.angle += m.degrees(delta_angle)

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
        self.angle_braquage = 0


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

    def mesurer_distance_obstacle(self, environnement, objects):
        """ Simule un capteur infrarouge détectant la distance jusqu'à un obstacle devant le véhicule """
        capteur_x = (self.r_Avg[0] + self.r_Avd[0]) / 2  # Position centrale entre les roues avant
        capteur_y = (self.r_Avg[1] + self.r_Avd[1]) / 2

        max_distance = 300  # Portée max du capteur
        pas = 5  # Distance entre chaque point de détection
        direction_angle = m.radians(self.angle)  # Convertir l'angle en radians

        for d in range(0, max_distance, pas):
            point_x = capteur_x + d * m.cos(direction_angle)
            point_y = capteur_y + d * m.sin(direction_angle)

            for obj in objects:  # Vérifier si ce point touche un obstacle
                if obj.collidepoint(point_x, point_y):
                    return d  # Retourne la distance au premier obstacle

        return max_distance  # Aucune collision détectée