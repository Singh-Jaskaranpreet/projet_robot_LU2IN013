from src.robot_général import Robot

class AdaptateurRR(Robot):
    def __init__(self,vehicule):
        self.vehicule=vehicule
    
    def avancer(valeur):
        vehicule.set_motor_dps(3, valeur)

    def arreter():
        vehicule.stop()

    def v_roue_gauche(valeur):
        vehicule.set_motor_dps(1, valeur)

    def v_roue_droite(valeur):
        vehicule.set_motor_dps(2, valeur)

    def distance_parcouru(vit,temps):
        position = self.vehicule.get_motor_position()
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        self.vehicule.offset_motor_encode(3,self.read_encoders())
        return (distance_droite + distance_gauche) / 2
    
    def get_distance(self):
        return self.vehicule.get_distance() / 1000

    def get_temps(vitesse):
        return distance_parcouru(vitesse,0) / vitesse

    def get_essieux():
        return vehicule.WHEEL_BASE_WIDTH