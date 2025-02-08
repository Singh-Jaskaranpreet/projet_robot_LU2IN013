import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, p_centre,empattement,essieux,):
        self.nom = nom
        self.long=empattement
        self.essieux = essieux
        self.angle = 0
        self.p_centre = p_centre
        self.vit_Rg = 0
        self.vit_Rd = 0
        self.starting_point_x=p_centre[0]
        self.starting_point_y=p_centre[1]
        self.nb_roues = 3

    #Place les trois roues de la voiture
    def position_des_roues(self, point):
        hyp = self.long / m.cos(m.radians(20))
        r_Ar = [point[0] - (self.long//2) * m.cos(m.radians(self.angle)), point[1] - (self.long//2) * m.sin(m.radians(self.angle))]
        r_Avg = [point[0] + hyp * m.cos(m.radians(self.angle + 20)), point[1] + hyp * m.sin(m.radians(self.angle + 20))]
        r_Avd = [r_Ar[0] + hyp * m.cos(m.radians(self.angle - 20)), r_Ar[1] + hyp * m.sin(m.radians(self.angle - 20))]
        return [r_Ar, r_Avg, r_Avd]
    
    def accelerer(self, val):
        self.vit_Rg = min(150,self.vit_Rg+val)
        self.vit_Rd = min(150,self.vit_Rd+val)
    
    def freiner(self, val):
        self.vit_Rg = max(0,self.vit_Rg-val)
        self.vit_Rd = max(0,self.vit_Rd-val)

    def bouger(self, environnement, objects, temps):
        """Déplace le véhicule en tenant compte des collisions et des limites."""
        tmp=self.angle

        vit_moyenne=(self.vit_Rd+self.vit_Rg)/2


        if self.vit_Rd == self.vit_Rd :
            prochain_pos = [
                self.p_centre[0] + vit_moyenne * m.cos(m.radians(self.angle)) * temps,
                self.p_centre[1] + vit_moyenne * m.sin(m.radians(self.angle)) * temps
            ]   

        if environnement.collision_predeplacement(prochain_pos):
            self.vit_Rg = 0
            self.vit_Rd = 0
            self.angle = tmp
            return       

        # Appliquer les nouvelles coordonnées si aucune collision
        self.p_centre = prochain_pos


    def tourner(self, direction, temps):
        """ Gère le braquage des roues en fonction de la direction,
        mais empêche l' angle si la roue arrière est bloquée. """
        if direction == "gauche":
            self.vit_Rg = 0
            omega = self.vit_Rd / self.essieux #vitesse angulaire
            self.angle += m.degrees(omega* temps)
        elif direction == "droite":
            self.vit_Rd = 0
            omega = -self.vit_Rg / self.essieux
            self.angle += m.degrees(omega* temps)


    def restart(self):
        self.p_centre=[self.starting_point_x,self.starting_point_y]
        self.angle = 0
        self.vit_Rd=0
        self.vit_Rg=0
        
        


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
                        print(f" Détection d'un obstacle rectangulaire à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

                # 🔵 Cas 2 : L'obstacle est un objet avec `x`, `y` et un `rayon` (cercle)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "rayon"):
                    distance_objet = m.sqrt((point_x - obj.x) ** 2 + (point_y - obj.y) ** 2)
                    if distance_objet <= obj.rayon:
                        print(f" Détection d'un obstacle circulaire à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

                # 🟢 Cas 3 : L'obstacle est un objet sans `pygame.Rect` mais avec `width` et `height` (rectangle custom)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "width") and hasattr(obj, "height"):
                    if (obj.x <= point_x <= obj.x + obj.width) and (obj.y <= point_y <= obj.y + obj.height):
                        print(f" Détection d'un obstacle rectangle custom à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté

        print(f" Aucun obstacle détecté, distance max : {max_distance}", end = "\r")
        return max_distance  # Aucune collision détectée