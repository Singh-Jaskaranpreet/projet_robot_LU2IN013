import math
from vehicule import *

class Environnement:

    def __init__(self, largeur, hauteur, vehicule, objects):
        """
        Initialise l'environnement avec la largeur et la hauteur spécifiées.
        """
        self.largeur = largeur
        self.hauteur = hauteur
        self.vehicule = vehicule
        self.objects = objects  #Liste des objets


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

    def collision_predeplacement(self, point):
        """
        Vérifie si une collision se produira lors du prochain déplacement du véhicule.
        Retourne True si une collision est détectée, sinon False.
        """
        # Points actuels du véhicule
        points_triangle = self.vehicule.position_des_roues(point)

        # Vérifier les collisions avec les objets
        for obj in self.objects:
            for t_edge in [
                    (points_triangle[0], points_triangle[1]),
                    (points_triangle[1], points_triangle[2]),
                    (points_triangle[2], points_triangle[0]),
            ]:
                if (len(obj) > 2):
                    t = len(obj)
                    for i in range(0 , t):
                        if self.segments_intersect(t_edge, (obj[i], obj[(i+1)%t])):
                            return True  # Collision détectée

        return False  # Pas de collision

    def rester_dans_limites(self):
        """ Empêche le véhicule de sortir de l'écran et arrête sa vitesse. """
        for point in self.vehicule.position_des_roues(self.vehicule.p_centre):
            if point[0] < 0 or point[0] > self.largeur   or point[1] < 0 or point[1] > self.hauteur :
                self.vehicule.restart()
                return
        return

    def add_objet(self,objet):
        """Ajoute l'objet dans l'environnement
            :param objet: l'objet a ajouter
            :return: rien
        """
        self.objects.append(objet)


