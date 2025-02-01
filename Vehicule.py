import pygame
import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, vitesse,coord, longueur, nb_roues):
        self.nom = nom
        self.long=longueur/2 # Distance entre les essieux
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

        # Vérifier si la roue arrière est bloquée
        roue_ar_bloquee = environnement.collision_roue_arriere(self, objects)

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
        collision_avant = environnement.collision_predeplacement(prochain_triangle, objects)

        # 🔄 Appliquer la rotation UNIQUEMENT si aucune collision détectée
        if self.angle_braquage != 0 and (not roue_ar_bloquee or not collision_avant):
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
        """ Simule un capteur infrarouge détectant la distance jusqu'au premier obstacle en face du véhicule. """
    
        # 🔹 Position du capteur (au centre des roues avant)
        capteur_x = (self.r_Avg[0] + self.r_Avd[0]) / 2
        capteur_y = (self.r_Avg[1] + self.r_Avd[1]) / 2

        # 🔹 Paramètres du capteur
        max_distance = 1000  # Distance maximale du capteur (en pixels)
        pas = 5  # Précision du scan (plus petit = plus précis)
        direction_angle = m.radians(self.angle)  # Convertir l'angle en radians

        print(f"\n📡 Capteur placé en ({capteur_x:.2f}, {capteur_y:.2f}) avec un angle de {self.angle}°")
        print(f"🔍 Nombre d'obstacles détectés : {len(objects)}")

        # 🔹 Scanner point par point en ligne droite
        for d in range(0, max_distance, pas):
            point_x = capteur_x + d * m.cos(direction_angle)
            point_y = capteur_y + d * m.sin(direction_angle)

            print(f"📡 Scan en ({point_x:.2f}, {point_y:.2f}) pour d={d}")

            # Vérifier si ce point touche un obstacle
            for obj in objects:
                # 🔴 Cas 1 : L'obstacle est un `pygame.Rect`
                if isinstance(obj, pygame.Rect):
                    if obj.collidepoint(point_x, point_y):
                        print(f"🚨 Détection d'un obstacle rectangulaire à {d} px !")
                        return d  # Distance au premier obstacle détecté

                # 🔵 Cas 2 : L'obstacle est un objet avec `x`, `y` et un `rayon` (cercle)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "rayon"):
                    distance_objet = m.sqrt((point_x - obj.x) ** 2 + (point_y - obj.y) ** 2)
                    if distance_objet <= obj.rayon:
                        print(f"🚨 Détection d'un obstacle circulaire à {d} px !")
                        return d  # Distance au premier obstacle détecté

                # 🟢 Cas 3 : L'obstacle est un objet sans `pygame.Rect` mais avec `width` et `height` (rectangle custom)
                elif hasattr(obj, "x") and hasattr(obj, "y") and hasattr(obj, "width") and hasattr(obj, "height"):
                    if (obj.x <= point_x <= obj.x + obj.width) and (obj.y <= point_y <= obj.y + obj.height):
                        print(f"🚨 Détection d'un obstacle rectangle custom à {d} px !")
                        return d  # Distance au premier obstacle détecté

        print(f"✅ Aucun obstacle détecté, distance max : {max_distance}")
        return max_distance  # Aucune collision détectée