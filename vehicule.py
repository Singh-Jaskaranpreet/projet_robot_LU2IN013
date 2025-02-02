import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse, p_centre ,longueur, nb_roues):
        self.nom = nom
        self.long=longueur/2 # Distance entre les essieux
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
        """Déplace le véhicule en tenant compte des collisions et des limites."""


        # Vérifier si la roue arrière est bloquée
        roue_ar_bloquee = environnement.collision_roue_arriere(self, objects)

        prochain_pos = [
            self.p_centre[0] + self.vitesse * m.cos(m.radians(self.angle)),
            self.p_centre[1] + self.vitesse * m.sin(m.radians(self.angle))
        
        ]

        if environnement.collision_predeplacement(self, prochain_pos, objects):
            self.vitesse = 0
            return

        # 🛑 Vérification spécifique : roue arrière bloquée en reculant
        if self.vitesse < 0 and environnement.collision_roue_arriere(self, objects):
            self.vitesse = 0
            return  # 🚨 Empêche complètement la rotation et le mouvement
        
        self.p_centre = prochain_pos

        if self.angle_braquage != 0 and (not roue_ar_bloquee or not environnement.collision_predeplacement(self,prochain_pos, objects)):
            rayon_courbure = self.long / m.tan(m.radians(self.angle_braquage))
            delta_angle = self.vitesse / rayon_courbure
            self.angle += m.degrees(delta_angle)

        # Appliquer les nouvelles coordonnées si aucune collision

    def tourner(self, direction, environnement, objects):
        """ Gère le braquage des roues en fonction de la direction,
        mais empêche la rotation si la roue arrière est bloquée. """
        if direction == "gauche":
            self.angle_braquage = max(self.angle_braquage - 1.5, -45)
        elif direction == "droite":
            self.angle_braquage = min(self.angle_braquage + 1.5, 45)


    def restart(self):
        self.p_centre=[self.starting_point_x,self.starting_point_y]
        self.angle = 0
        self.direction_x = 1
        self.direction_y = 0
        self.vitesse=0
        self.angle_braquage = 0
        self.angle = 0


    def bouger_retour(self):
        """
        Recule légèrement pour empêcher le véhicule d'entrer dans un obstacle.
        """
        self.p_centre[0] -= self.vitesse * self.direction_x
        self.p_centre[1] -= self.vitesse * self.direction_y


    def mesurer_distance_obstacle(self, environnement, objects):
        """ Simule un capteur infrarouge détectant la distance jusqu'au premier obstacle en face du véhicule. """
    
        # 🔹 Position du capteur (au centre des roues avant)
        roues = self.position_des_roues(self.p_centre)
        capteur_x = (roues[1][0] + roues[2][0]) / 2
        capteur_y = (roues[1][1] + roues[2][1]) / 2

        # 🔹 Paramètres du capteur
        max_distance = 1000  # Distance maximale du capteur (en pixels)
        pas = 5  # Précision du scan (plus petit = plus précis)
        direction_angle = m.radians(self.angle)  # Convertir l'angle en radians

        # 🔹 Scanner point par point en ligne droite
        for d in range(0, max_distance, pas):
            point_x = capteur_x + d * m.cos(direction_angle)
            point_y = capteur_y + d * m.sin(direction_angle)

            # Vérifier si ce point touche un obstacle
            for obj in objects:
                # 🔴 Cas 1 : L'obstacle est un `pygame.Rect`
                if isinstance(obj, pygame.Rect):
                    if obj.collidepoint(point_x, point_y):
                        print(f"🚨 Détection d'un obstacle rectangulaire à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

                # 🔵 Cas 2 : L'obstacle est un objet avec `x`, `y` et un `rayon` (cercle)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "rayon"):
                    distance_objet = m.sqrt((point_x - obj.x) ** 2 + (point_y - obj.y) ** 2)
                    if distance_objet <= obj.rayon:
                        print(f"🚨 Détection d'un obstacle circulaire à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

                # 🟢 Cas 3 : L'obstacle est un objet sans `pygame.Rect` mais avec `width` et `height` (rectangle custom)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "width") and hasattr(obj, "height"):
                    if (obj.x <= point_x <= obj.x + obj.width) and (obj.y <= point_y <= obj.y + obj.height):
                        print(f"🚨 Détection d'un obstacle rectangle custom à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

        print(f"✅ Aucun obstacle détecté, distance max : {max_distance}", end = "\r")
        return max_distance  # Aucune collision détectée