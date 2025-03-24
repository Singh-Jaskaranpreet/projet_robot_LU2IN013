from .robotGeneral import Robot
import config

class AdaptateurRR(Robot):
    def __init__(self,vehicule):
        """
        Constructeur de la classe AdaptateurRR
        :param vehicule: VehiculeR
        """
        self.vehicule=vehicule
        self.vitesse_RG = config.VITESSE_RG
        self.vitesse_RD = config.VITESSE_RD
        self.sequence = config.SEQUENCE

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

    def set_VrG(self,valeur):
        """
        Donne une vitesse à la roues gauche
        :param valeur: float
        :return None
        """
        self.vehicule.set_motor_dps(1, valeur)
        self.vitesse_RG = valeur

    def set_VrD(self,valeur):
        """
        Donne une vitesse à la roues droite
        :param valeur: float
        :return None
        """
        self.vehicule.set_motor_dps(2, valeur)
        self.vitesse_RD = valeur

    def get_distance_parcouru(self, vit=0):
        """
        Retourne la distance parcourue par le robot
        :return float
        """
        print("on renvoie la ditance parcouru")
        position = self.vehicule.get_motor_position()
        print(position)
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE )#/ 1000 ) je les ai enlever pour le test sinon c'etais beaucoup trop long
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE )#/ 1000 )
        self.reset()
        if distance_droite < 0.01 :
            return distance_gauche
        elif distance_gauche < 0.01 :
            return distance_droite   
        return (distance_droite + distance_gauche) / 2
    
    def get_distance_to_obstacle(self):
        """
        Retourne la distance par rapport à un obstacle devant lui
        :return float
        """
        return 50 #self.vehicule.get_distance() / 1000 comme on a return 1000 est qu eon divise par 1000 on a 1 se qui arrete les execution des stratégy

    def get_temps(self):
        """
        Retourne le temps écoulé 
        :return float
        """
        if self.get_VrD() < 0.01:
            print(f'il sest écoulé{self.get_distance_parcouru() / self.get_VrG()}')
            return self.get_distance_parcouru() / self.get_VrG()
        if self.get_VrG() < 0.01:
            print(f'il sest écoulé{self.get_distance_parcouru() / self.get_VrD()}')
            return self.get_distance_parcouru() / self.get_VrD()
        print(f'il sest écoulé{self.get_distance_parcouru() / ((self.get_VrD() + self.get_VrG())/2)}')
        return self.get_distance_parcouru() / ((self.get_VrD() + self.get_VrG())/2)

    def get_essieux(self):
        """
        Retourne la distance entre les deux roues du robot
        :return float
        """
        return self.vehicule.WHEEL_BASE_WIDTH

    def get_VrG(self):
        """
        Retourne la vitesse de la roue gauche
        :return float
        """
        return self.vitesse_RG

    def get_VrD(self):
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
        self.vehicule.offset_motor_encoder(3, 0)#self.vehicule.read_encoders()[0]) #ne fonctionne pas avec self.vehicule.read_encoders[0]

    def get_angle_parcourueRad(self,vitesse):
       """
       Retourne l'angle parcourue lors de la rotation"
       :return float
       """
       return super().get_angle_parcourueRad(vitesse)
    