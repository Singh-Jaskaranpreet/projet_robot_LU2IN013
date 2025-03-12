
class AdaptateurVF:
    def __init__(self,vehicule):
        self.vehicule=vehicule
    
    def distance_parcouru(self,vit,temps):
        position = self.vehicule.get_motor_position()
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        self.vehicule.offset_motor_encode(3,self.read_encoders())
        return (distance_droite + distance_gauche) / 2
    
    def get_distance(self):
        return self.vehicule.get_distance() / 1000