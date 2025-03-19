import math as m
from src.modele import Vehicule
from .horloge import Horloge
from random import randint, uniform, random

class Environnement:

    def __init__(self):
        """
        Initialise l'environnement avec la largeur et la hauteur spécifiées.
        :param largeur: Largeur de l'environnement
        :param hauteur: Hauteur de l'environnement
        :param vehicule: Véhicule à contrôler
        :param objects: Liste des objets dans l'environnement
        :param temps: Horloge pour mesurer le temps écoulé
        :param traces: Liste des positions précédentes du véhicule
        :param trace_active: Indique si le traçage est actif
        :param asuivre: Liste des positions à suivre
        :param direction_cible: Direction actuelle de la cible
        :param speed_target: Vitesse de la cible
        :param asuivre_act: Indique si la cible est active
        """
        self.largeur = 1200
        self.hauteur = 800
        self.vehicule = Vehicule("Robot",[200, 400] , 50, 40,self)
        #self.objects = [[(400,100),(600,100),(600,600),(400,600)]]  #Liste des objets
        #self.objects = [((400,600),60)] #pour pas avoir d'obstacle
        self.objects = [] #pour pas avoir d'obstacle
        self.temps = Horloge()
        self.traces = []
        self.trace_active = False
        self.asuivre = [(randint(100, self.largeur - 100), randint(100, self.hauteur - 100))]  # Position initiale aléatoire
        self.direction_cible = uniform(0, 360)  # Angle initial aléatoire en degrés
        self.speed_target = 500  # Vitesse de la cible en pixels/s
        self.asuivre_act = False

    def segments_intersect(self, seg1, seg2):
        """
        Vérifie si deux segments (seg1 et seg2) s'intersectent.
        :param seg1: Est un segment
        :param seg2: Est un segment
        """
        def orientation(p, q, r):
            """
            Calcule l'orientation du triplet de points (p, q, r).
            Retourne 0 si colinéaire, 1 pour anti-horaire et -1 pour horaire.
            :param p: Premier point
            :param q: Deuxième point
            :param r: Troisième point
            :return: Orientation du triplet de points
            """
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # Colinéaire
            return 1 if val > 0 else -1

        def on_segment(p, q, r):
            """
            Vérifie si le point q est sur le segment pr.
            :param p: Premier point du segment
            :param q: Point à vérifier
            :param r: Deuxième point du segment
            :return: True si q est sur le segment pr, sinon False
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

    
    def segment_cercle_collision(self, seg, centre, rayon):
        """ 
        Vérifie si un segment intersecte un cercle. 
        :param seg: Segment à vérifier
        :param centre: Centre du cercle
        :param rayon: Rayon du cercle
        :return: True si le segment intersecte le cercle, sinon False
        """
        A, B = seg
        Cx, Cy = centre

        # Vecteur du segment
        ABx, ABy = B[0] - A[0], B[1] - A[1]
        ACx, ACy = Cx - A[0], Cy - A[1]

        # Projection du point sur le segment
        t = max(0, min(1, (ACx * ABx + ACy * ABy) / (ABx**2 + ABy**2)))
        Px, Py = A[0] + t * ABx, A[1] + t * ABy

        # Distance entre le point projeté et le centre du cercle
        distance = m.sqrt((Px - Cx)**2 + (Py - Cy)**2)
        
        return distance <= rayon

    
    
    def collision(self):
        """
        Vérifie si une collision se produira lors du prochain déplacement du véhicule.
        Retourne True si une collision est détectée, sinon False.
        :return: Les points en collision sinon False
        """
        # Points actuels du véhicule
        points_triangle = self.vehicule.position_des_roues(self.vehicule.p_centre)

        # Partie du vehicule qui sont en collision
        point_collision =set()

        # Indice du segment en collsion
        indice = 0

        segments_vehicule = [
        (points_triangle[0], points_triangle[1]),
        (points_triangle[1], points_triangle[2]),
        (points_triangle[2], points_triangle[0])
        ]

        # Vérifier les collisions avec les objets
        for obj in self.objects:
            for point in points_triangle :
                if len(obj) == 4 :
                    if (obj[0][0] <= point[0] <= obj[2][0]) and (obj[0][1] <= point[1] <= obj[2][1]):
                        point_collision.add(indice)
                        break
                elif len(obj) == 2:  # 🔵 Cas d'un obstacle circulaire
                    centre, rayon = obj
                    for seg in segments_vehicule:
                        if self.segment_cercle_collision(seg, centre, rayon):
                            return True

                    return False
                indice = indice + 1
            if len(point_collision) > 0 :
                break 

            #On prend chaque coté du vehicule
            cote = [(points_triangle[0], points_triangle[1]),(points_triangle[1], points_triangle[2]),(points_triangle[2], points_triangle[0])]
                   
            for t_edge in cote:
                if (len(obj) >= 2):
                    t = len(obj)
                    for i in range(0 , t):
                        if self.segments_intersect(t_edge, (obj[i], obj[(i+1)%t])):
                            point_collision.add(indice)
                indice = indice+1
            if len(point_collision) > 0 :
                break
        if len(point_collision)>0:
            return point_collision
        return False       

    def correction_apres_collision(self,segment):
        """
        Corrige la position du véhicule.
        :param segment: côté du véhicule en collision
        """
        angle = self.vehicule.angle

        if self.vehicule.vit_Rd > self.vehicule.vit_Rg :
            if segment == {1} or segment == {3} :
                angle = angle + 90
            else :
                angle = angle - 90
        if self.vehicule.vit_Rd < self.vehicule.vit_Rg :
            if segment == {2} or segment == {5} :
                angle = angle - 90
            else :
                angle = angle + 90
        if segment == {3,5} or segment == {0} :
            pos = [
                self.vehicule.p_centre[0] + 0.01 * m.cos(m.radians(angle)),
                self.vehicule.p_centre[1] + 0.01 * m.sin(m.radians(angle))
            ]
        else :
            pos = [
                self.vehicule.p_centre[0] - 0.01 * m.cos(m.radians(angle)),
                self.vehicule.p_centre[1] - 0.01 * m.sin(m.radians(angle))
            ]
        self.vehicule.p_centre = pos      

    def rester_dans_limites(self):
        """ 
        Empêche le véhicule de sortir de l'écran et arrête sa vitesse. 
        """
        for point in self.vehicule.position_des_roues(self.vehicule.p_centre):
            if point[0] < 0 or point[0] > self.largeur   or point[1] < 0 or point[1] > self.hauteur :
                self.vehicule.vit_Rd = 0
                self.vehicule.vit_Rg = 0
            if point[0] < -1 or point[0] > self.largeur +1   or point[1] < -1 or point[1] > self.hauteur +1 :
                self.restart()
        
        return

    def add_objet(self,objet):
        """
        Ajoute l'objet dans l'environnement
        :param objet: l'objet a ajouter
        """
        self.objects.append(objet)


    def bouger(self):
        """
        Déplace le véhicule selon le modèle cinématique différentiel pendant un pas de temps.
        :return: Les points en collision sinon False
        """
        collision = self.collision()
        dt = self.temps.get_temps_ecoule()
        
        if not collision:
            # Calcul de la vitesse linéaire moyenne et de la vitesse angulaire
            v = (self.vehicule.vit_Rg + self.vehicule.vit_Rd) / 2.0
            omega = (self.vehicule.vit_Rd - self.vehicule.vit_Rg) / self.vehicule.essieux

            # Mise à jour de l'angle (attention : angle en degrés)
            # omega est en rad/s, on le convertit en degrés
            dtheta_deg = m.degrees(omega * dt)
            self.vehicule.angle = (self.vehicule.angle + dtheta_deg) % 360
            
            # Mise à jour de la position
            # La position est mise à jour en fonction de l'orientation actuelle du véhicule
            theta_rad = m.radians(self.vehicule.angle)
            dx = v * m.cos(theta_rad) * dt
            dy = v * m.sin(theta_rad) * dt
            self.vehicule.p_centre[0] += dx
            self.vehicule.p_centre[1] += dy
        
        else:
            # En cas de collision, on arrête le véhicule et on corrige sa position
            self.vehicule.vit_Rd = 0
            self.vehicule.vit_Rg = 0
            self.correction_apres_collision(collision)
    

    def restart(self):
        """
        Reinitiallise la position du vehicule et ses attributs 
        """
        self.vehicule.p_centre=[self.vehicule.starting_point_x,self.vehicule.starting_point_y]
        self.vehicule.angle = 0
        self.vehicule.vit_Rd=0
        self.vehicule.vit_Rg=0

    def tracer_ligne(self):
        """
        Ajoute la position actuelle du véhicule à la liste des traces.
        """
        if self.trace_active:
            self.traces.append(tuple(self.vehicule.p_centre))

    def effacer_ligne(self):
        """Efface toutes les traces du véhicule."""
        self.traces = []

    def basculer_tracage(self):
        """
        Active ou désactive le traçage.
        """
        self.trace_active = not self.trace_active  # Bascule entre True et False

    def bouger_cible(self):
        """
        Déplace la cible aléatoirement en changeant de direction parfois.
        """
        if not self.asuivre:
            return
        dt = self.temps.get_temps_ecoule()
        x, y = self.asuivre[0]

        # Changer la direction de la cible de manière aléatoire (avec faible probabilité)
        if random() < 0.02:  # 2% de chance par frame de changer de direction
            self.direction_cible += uniform(-45, 45)  # Variation aléatoire entre -45° et 45°

        # Convertir l'angle en mouvement (vx, vy)
        vx = self.speed_target * m.cos(m.radians(self.direction_cible)) * dt
        vy = self.speed_target * m.sin(m.radians(self.direction_cible)) * dt

        # Mise à jour de la position
        x += vx
        y += vy

        # Vérifier les bords et rebondir
        if x <= 50 or x >= self.largeur - 50:
            self.direction_cible = 180 - self.direction_cible  # Inversion horizontale
        if y <= 50 or y >= self.hauteur - 50:
            self.direction_cible = -self.direction_cible  # Inversion verticale

        # Mise à jour de la position de la cible
        self.asuivre[0] = (x, y)