import math
from vehicule import *

class Environnement:

    def __init__(self):
        """
        Initialise l'environnement avec la largeur et la hauteur spécifiées.
        """
        self.largeur = 1200
        self.hauteur = 800
        self.vehicule = Vehicule("Robot",[200, 400] , 50, 50)
        self.objects = [[(400,100),(600,100),(600,600),(400,600)]]  #Liste des objets
        #self.objects = [] #pour pas avoir d'obstacle

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

    def collision(self, rec):
        """
        Vérifie si une collision se produira lors du prochain déplacement du véhicule.
        Retourne True si une collision est détectée, sinon False.
        """
        # Points actuels du véhicule
        points_triangle = self.vehicule.position_des_roues(self.vehicule.p_centre)

        # Partie du vehicule qui sont en collision
        point_collision =set()

        # Indice du segment en collsion
        indice = 0

        # Vérifier les collisions avec les objets
        for obj in self.objects:
            for point in points_triangle :
                if len(obj) == 4 :
                    if (obj[0][0] <= point[0] <= obj[2][0]) and (obj[0][1] <= point[1] <= obj[2][1]):
                        point_collision.add(indice)
                        break
                indice = indice + 1
            if len(point_collision) > 0 :
                break
            indice = 0            
            for t_edge in [
                    (points_triangle[0], points_triangle[1]),
                    (points_triangle[1], points_triangle[2]),
                    (points_triangle[2], points_triangle[0]),
            ]:
                if (len(obj) > 2):
                    t = len(obj)
                    for i in range(0 , t):
                        if self.segments_intersect(t_edge, (obj[i], obj[(i+1)%t])):
                            point_collision.add(indice)
                indice = indice+1
            if len(point_collision) > 0 :
                break
        if rec == 1 and len(point_collision)==0 :
            self.vehicule.vit_Rd = 0
            self.vehicule.vit_Rg = 0
        if len(point_collision)>0:
            self.correction_apres_collision(point_collision)
            self.collision(1)
        

    def correction_apres_collision(self,segment):
        """
        Corrige la position du véhicule.
        :param segment: côté du véhicule en collision
        :param tourner: savoir si le véhicule a tourné  
        """
        angle = self.vehicule.angle

        if self.vehicule.vit_Rd > self.vehicule.vit_Rg :
            if segment == {1}:
                angle = angle + 90
            else :
                angle = angle - 90
        if self.vehicule.vit_Rd < self.vehicule.vit_Rg :
            if segment == {2}:
                angle = angle - 90
            else :
                angle = angle + 90
        if segment == {0,2} or segment == {0} :
            pos = [
                self.vehicule.p_centre[0] + 0.02 * m.cos(m.radians(angle)),
                self.vehicule.p_centre[1] + 0.02 * m.sin(m.radians(angle))
            ]
        else :
            pos = [
                self.vehicule.p_centre[0] - 0.02 * m.cos(m.radians(angle)),
                self.vehicule.p_centre[1] - 0.02 * m.sin(m.radians(angle))
            ]
        self.vehicule.p_centre = pos      

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


