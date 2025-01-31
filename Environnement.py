import pygame
import math
from time import sleep 

class Environnement:

    def __init__(self, largeur, hauteur):
        """
        Initialise l'environnement avec la largeur et la hauteur spécifiées.
        """
        self.largeur = largeur
        self.hauteur = hauteur

    def mise_a_jour(self, vehicule):
        """
        Met à jour l'état de l'environnement. Si le véhicule est trop proche des bords de l'écran,
        il est arrêté.
        """
        # Arrêter le véhicule si proche du bord droit
        if (vehicule.r_Avg[0] + 10 > self.largeur or vehicule.r_Avd[0] + 10 > self.largeur or vehicule.r_Ar[0] + 10 > self.largeur):
            vehicule.arret()
        if (vehicule.r_Avg[0] > self.largeur or vehicule.r_Avd[0] > self.largeur or vehicule.r_Ar[0] > self.largeur):
            vehicule.restart()

        # Arrêter le véhicule si proche du bord gauche
        if (vehicule.r_Avg[0] - 10 < 0 or vehicule.r_Avd[0] - 10 < 0 or vehicule.r_Ar[0] - 10 < 0):
            vehicule.arret()
        if (vehicule.r_Avg[0] < 0 or vehicule.r_Avd[0] < 0 or vehicule.r_Ar[0] < 0):
            vehicule.restart()

        # Arrêter le véhicule si proche du bord bas
        if (vehicule.r_Avg[1] + 10 > self.hauteur or vehicule.r_Avd[1] + 10 > self.hauteur or vehicule.r_Ar[1] + 10 > self.hauteur):
            vehicule.arret()
        if (vehicule.r_Avg[1] > self.hauteur or vehicule.r_Avd[1] > self.hauteur or vehicule.r_Ar[1] > self.hauteur):
            vehicule.restart()

        # Arrêter le véhicule si proche du bord haut
        if (vehicule.r_Avg[1] - 10 < 0 or vehicule.r_Avd[1] - 10 < 0 or vehicule.r_Ar[1] - 10 < 0):
            vehicule.arret()
        if (vehicule.r_Avg[1] < 0 or vehicule.r_Avd[1]  < 0 or vehicule.r_Ar[1] < 0):
            vehicule.restart()


    def segments_intersect(self, seg1, seg2):
        """
        Vérifie si deux segments (seg1 et seg2) s'intersectent.
        Chaque segment est défini par deux points : ((x1, y1), (x2, y2))
        """
        def orientation(p, q, r):
            """
            Calcule l'orientation du triplet de points (p, q, r).
            Retourne 0 si colinéaire, 1 pour anti-horaire et -1 pour horaire.
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Colinéaire
            return 1 if val > 0 else -1

        def on_segment(p, q, r):
            """
            Vérifie si le point q est sur le segment pr.
            """
            return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0])) and (min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

        p1, q1 = seg1
        p2, q2 = seg2

        # Calcul des orientations
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # Cas général (les segments se croisent)
        if o1 != o2 and o3 != o4:
            return True

        # Cas particuliers : segments colinéaires
        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False

    def collision_predeplacement(self, vehicule, objects):
        """
        Vérifie si une collision se produira lors du prochain déplacement du véhicule.
        Retourne True si une collision est détectée, sinon False.
        """
        # Points actuels du véhicule
        points_triangle = [
            vehicule.r_Ar,
            vehicule.r_Avg,
            vehicule.r_Avd,
        ]

        # Prochaines positions en fonction de la vitesse
        prochain_points_triangle = [
            [p[0] + vehicule.vitesse * vehicule.direction_x, p[1] + vehicule.vitesse * vehicule.direction_y]
            for p in points_triangle
        ]

        # Vérifier les collisions avec les objets
        for obj in objects:
            # Convertir l'obstacle en segments
            rectangle_edges = [
                (obj.topleft, obj.topright),
                (obj.topright, obj.bottomright),
                (obj.bottomright, obj.bottomleft),
                (obj.bottomleft, obj.topleft),
            ]

            # Vérifier la collision avec chaque arête du triangle
            for t_edge in [
                    (prochain_points_triangle[0], prochain_points_triangle[1]),
                    (prochain_points_triangle[1], prochain_points_triangle[2]),
                    (prochain_points_triangle[2], prochain_points_triangle[0]),
            ]:
                for r_edge in rectangle_edges:
                    if self.segments_intersect(t_edge, r_edge):
                        print("oh là là le pare choc!! My G-WAGON")
                        return True

        return False

    def corriger_position_apres_collision(self, vehicule, objects):
        """
        Corrige la position du véhicule si une collision est détectée.
        Le véhicule sera repositionné juste avant de toucher l'obstacle.
        """
        points_triangle = [
            vehicule.r_Ar,
            vehicule.r_Avg,
            vehicule.r_Avd
        ]

        # Vérifier les collisions et repositionner le véhicule si nécessaire
        for obj in objects:
            rectangle_edges = [
                (obj.topleft, obj.topright),
                (obj.topright, obj.bottomright),
                (obj.bottomright, obj.bottomleft),
                (obj.bottomleft, obj.topleft),
            ]

            # Vérifier chaque arête du triangle
            for t_edge in [
                    (points_triangle[0], points_triangle[1]),
                    (points_triangle[1], points_triangle[2]),
                    (points_triangle[2], points_triangle[0]),
            ]:
                for r_edge in rectangle_edges:
                    if self.segments_intersect(t_edge, r_edge):
                        # Repositionner le véhicule juste avant l'obstacle
                        vehicule.bouger_retour()  # Déplace le véhicule en arrière
                        return True

        return False

    def collision_pre_rotation(self, nouveau_triangle, objects):
        """
        Vérifie si le triangle `nouveau_triangle` entrerait en collision
        avec l'un des obstacles lors d'une rotation.
        """
        for obj in objects:
            rectangle_edges = [
                (obj.topleft, obj.topright),
                (obj.topright, obj.bottomright),
                (obj.bottomright, obj.bottomleft),
                (obj.bottomleft, obj.topleft),
            ]

            # Vérifier les intersections entre le nouveau triangle et les arêtes du rectangle
            for t_edge in [
                    (nouveau_triangle[0], nouveau_triangle[1]),
                    (nouveau_triangle[1], nouveau_triangle[2]),
                    (nouveau_triangle[2], nouveau_triangle[0]),
            ]:
                for r_edge in rectangle_edges:
                    if self.segments_intersect(t_edge, r_edge):
                        return True  # Collision détectée, retour immédiat
        return False  # Aucune collision détectée
