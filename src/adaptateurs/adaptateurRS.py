from src.strategy import *
from src.robot_général import Robot


class AdaptateurRS(Robot):
    def __init__(self, vehicule):
        """
        Constructeur de la classe AdaptateurRS
        :param vehicule: VehiculeSimule
        :param mode: int
        """
        self.vehicule = vehicule
        self.choix = 2
        self.sequence = None

   
    def avancer(self,valeur):
        """
        Fait avancer le robot
        :param valeur: float
        :return: None
        """
        self.vehicule.set_vrd(valeur)
        self.vehicule.set_vrg(valeur)

    def arreter(self):
        """
        Arrête le robot
        :return: None
        """
        self.vehicule.set_vrd(0)
        self.vehicule.set_vrg(0)

    def v_roue_gauche(self,valeur):
        """
        Donne une vitesse à la roues gauche
        :param valeur: float
        :return None
        """
        self.vehicule.set_vrg(valeur)

    def v_roue_droite(self,valeur):
        """
        Donne une vitesse à la roues droite
        :param valeur: float
        :return None
        """
        self.vehicule.set_vrd(valeur)

    def distance_parcouru(self,vit):
        """
        Retourne la distance parcourue par le robot
        :return float
        """
        return abs(round(0.003*(abs((abs(vit)+abs(vit))/2)),3) * self.get_temps())
    
    def get_distance(self):
        """
        Retourne la distance par rapport à un obstacle devant lui
        :return float
        """
        return self.vehicule.infrarouge.mesurer_distance_obstacle(self.vehicule)

    def get_temps(self):
        """
        Retourne le temps écoulé
        :return float
        """
        return self.vehicule.environnement.temps.get_temps_ecoule()

    def get_essieux(self):
        """
        Retourne la distance entre les deux roues du robot
        :return float
        """
        return self.vehicule.essieux
    
    def get_centre(self):
        """
        Retourne la position du centre du robot
        :return tuple
        """
        return self.vehicule.p_centre

    def get_vitesse_Rg(self):
        """
        Retourne la vitesse de la roue gauche
        :return float
        """
        return self.vehicule.vit_Rg

    def get_vitesse_Rd(self):
        """
        Retourne la vitesse de la roue droite
        :return float
        """
        return self.vehicule.vit_Rd

    def reset(self):
        """
        Réinitialise les encodeurs
        :return None
        """
        self.v_roue_gauche(0)
        self.v_roue_droite(0)

    
    def faire_carre(self):
        """
        Fait faire un carré au robot
        :return None
        """
        self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(-90)] * 4)
        self.sequence.start(self.vehicule)

    def angle_parcourueRad(self,vitesse):
        """
        Retourne l'angle parcourue lors de la rotation
        :return float
        """
        return super().angle_parcourueRad(vitesse)
    

        

