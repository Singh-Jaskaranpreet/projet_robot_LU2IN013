from .robotGeneral import Robot


class AdaptateurRR(Robot):
    def __init__(self,vehicule):
        """
        Constructeur de la classe AdaptateurRR
        :param vehicule: VehiculeR
        """
        self.vehicule=vehicule
        self.vitesse_RG = 0
        self.vitesse_RD = 0
        self.sequence = None

    def avancer(self,valeur):
        """
        Fait avancer le robot
        :param valeur: float
        :return: None
        """
        self.vehicule.set_motor_dps(3, valeur)

    def arreter(self):
        """
        Arrête le robot
        :return: None
        """
        self.vehicule.stop()

    def v_roue_gauche(self,valeur):
        """
        Donne une vitesse à la roues gauche
        :param valeur: float
        :return None
        """
        self.vehicule.set_motor_dps(1, valeur)
        self.vitesse_RG = valeur

    def v_roue_droite(self,valeur):
        """
        Donne une vitesse à la roues droite
        :param valeur: float
        :return None
        """
        self.vehicule.set_motor_dps(2, valeur)
        self.vitesse_RD = valeur

    def distance_parcouru(self):
        """
        Retourne la distance parcourue par le robot
        :return float
        """
        position = self.vehicule.get_motor_position()
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        self.reset()
        if distance_droite < 0.01 :
            return distance_gauche
        elif distance_gauche < 0.01 :
            return distance_droite    
        return (distance_droite + distance_gauche) / 2
    
    def get_distance(self):
        """
        Retourne la distance par rapport à un obstacle devant lui
        :return float
        """
        return self.vehicule.get_distance() / 1000

    def get_temps(self):
        """
        Retourne le temps écoulé 
        :return float
        """
        if self.get_vitesse_Rd() < 0.01:
            return self.distance_parcouru() / self.get_vitesse_Rg()
        if self.get_vitesse_Rg() < 0.01:
            return self.distance_parcouru() / self.get_vitesse_Rd()
        return self.distance_parcouru() / ((self.get_vitesse_Rd() + self.get_vitesse_Rg())/2)

    def get_essieux(self):
        """
        Retourne la distance entre les deux roues du robot
        :return float
        """
        return self.vehicule.WHEEL_BASE_WIDTH

    def get_vitesse_Rg(self):
        """
        Retourne la vitesse de la roue gauche
        :return float
        """
        return self.vitesse_RG

    def get_vitesse_Rd(self):
        """
        Retourne la vitesse de la roue droite
        :return float
        """
        return self.vitesse_RD

    def reset(self):
        """
        Réinitialise les encodeurs
        :return None
        """

        self.vehicule.offset_motor_encode(3,self.read_encoders())

    def angle_parcourueRad(self,vitesse):
       """
       Retourne l'angle parcourue lors de la rotation"
       :return float
       """
       return super().angle_parcourueRad(vitesse)
    