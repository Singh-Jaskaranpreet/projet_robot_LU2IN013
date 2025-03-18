from src.robot_général import Robot
from src.strategy import *

class AdaptateurRR(Robot):
    def __init__(self,vehicule):
        self.vehicule=vehicule
        self.vitesse_RG = 0
        self.vitesse_RD = 0
        self.sequence = None

    def avancer(self,valeur):
        self.vehicule.set_motor_dps(3, valeur)

    def arreter(self):
        self.vehicule.stop()

    def v_roue_gauche(self,valeur):
        self.vehicule.set_motor_dps(1, valeur)
        self.vitesse_RG = valeur

    def v_roue_droite(self,valeur):
        self.vehicule.set_motor_dps(2, valeur)
        self.vitesse_RD = valeur

    def distance_parcouru(self):
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
        return self.vehicule.get_distance() / 1000

    def get_temps(self):
        if self.get_vitesse_Rd() < 0.01:
            return self.distance_parcouru() / self.get_vitesse_Rg()
        if self.get_vitesse_Rg() < 0.01:
            return self.distance_parcouru() / self.get_vitesse_Rd()
        return self.distance_parcouru() / ((self.get_vitesse_Rd() + self.get_vitesse_Rg())/2)

    def get_essieux(self):
        return self.vehicule.WHEEL_BASE_WIDTH

    def get_vitesse_Rg(self):
        return self.vitesse_RG

    def get_vitesse_Rd(self):
        return self.vitesse_RD

    def reset(self):
        self.vehicule.offset_motor_encode(3,self.read_encoders())

    def v_angulaire(self):
        return self.distance_parcouru() / ((self.get_vitesse_Rd + self.get_vitesse_Rg)/2)
    def get_angle(self):
        pass
    
    def faire_carre(self):
        self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
        self.sequence.start(self.vehicule)
