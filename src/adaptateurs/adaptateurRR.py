from src.robot_général import Robot

class AdaptateurRR(Robot):
    def __init__(self,vehicule):
        self.vehicule=vehicule
        self.vitesse_RG = 0
        self.vitesse_RD = 0
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

    def distance_parcouru(self,vit,temps):
        position = self.vehicule.get_motor_position()
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        self.vehicule.offset_motor_encode(3,self.read_encoders())
        return (distance_droite + distance_gauche) / 2
    
    def get_distance(self):
        return self.vehicule.get_distance() / 1000

    def get_temps(self,vitesse):
        return self.distance_parcouru(vitesse,0) / vitesse

    def get_essieux(self):
        return self.vehicule.WHEEL_BASE_WIDTH

    def get_vitesse_Rg(self):
        return self.vitesse_RG

    def get_vitesse_Rd(self):
        return self.vitesse_RD
