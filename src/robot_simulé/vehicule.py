from .outils import Infrarouge
import math as m

# Classe Véhicule
class Vehicule:

    def __init__(self, nom, p_centre,empattement,essieux,environnement,angle = 0):
        """
        Constructeur de la classe Vehicule
        :param nom: Le nom de la voiture
        :param angle: L'angle de la voiture
        :param p_centre: Le point central de la voiture
        :param empattement: La longueur de la voiture
        :param essieux: La largeur de la voiture
        :param environnement: L'environnement de la voiture (classe Environnement)
        :param angle: L'angle de la voiture
        :param vit_Rg: La vitesse de la roue gauche
        :param vit_Rd: La vitesse de la roue droite
        :param starting_point_x: Le point de départ en x
        :param starting_point_y: Le point de départ en y
        :param nb_roues: Le nombre de roues
        :param infrarouge: Le capteur infrarouge
        :param angle_servo: L'angle du servo
        """
        self.nom = nom
        self.long=empattement
        self.essieux = essieux
        self.angle = angle %360
        self.p_centre = p_centre
        self.vit_Rg = 0
        self.vit_Rd = 0
        self.starting_point_x=p_centre[0]
        self.starting_point_y=p_centre[1]
        self.nb_roues = 3
        self.environnement = environnement
        self.infrarouge = Infrarouge()
        self.angle_servo = 0

    
    def freiner(self, val):
        """
        Freine la voiture
        :param val: La valeur de freinage
        """
        if self.vit_Rg > 0:
            self.vit_Rg = max(0,self.vit_Rg-val)
        elif self.vit_Rg < 0:
            self.vit_Rg = min(0,self.vit_Rg+val)
        if self.vit_Rd > 0:
            self.vit_Rd = max(0,self.vit_Rd-val)
        elif self.vit_Rd < 0:
            self.vit_Rd = min(0,self.vit_Rd+val)

        
    def get_distance(self):
        """
        Renvoie la distance par rapport a un obstacle s'il existe.
        :return: float
        """
        return self.infrarouge.mesurer_distance_obstacle(self)
    
    def set_vrd(self, x):
        """
        Met la roue droite a une certaine vitesse.
        :param x: La vitesse de la roue droite est x
        """
        self.vit_Rd = x

    def set_vrg(self, x):
        """
        Met la roue gauche a une certaine vitesse.
        :param x: La vitesse de la roue gauche est x
        """
        self.vit_Rg = x


    def servo_rotate(self,position):
        """
        Fait tourner le servo
        :param position: La position du servo
        """
        self.angle_servo = max(-60, min(position, 60))
        

    #Place les trois roues de la voiture
    def position_des_roues(self, point):
        """
        Renvoie la position des roues
        :param point: Calcule de la position par rapport a point
        """
        r_Ar = [point[0] - self.long * m.cos(m.radians(self.angle)), point[1] - self.long * m.sin(m.radians(self.angle))]
        r_Avg = [point[0] + (self.essieux // 2) * m.cos(m.radians(self.angle + 90)), point[1] + (self.essieux // 2) * m.sin(m.radians(self.angle + 90))]
        r_Avd = [point[0] + (self.essieux // 2) * m.cos(m.radians(self.angle - 90)), point[1] + (self.essieux // 2) * m.sin(m.radians(self.angle - 90))]
        return [r_Ar, r_Avg, r_Avd]
