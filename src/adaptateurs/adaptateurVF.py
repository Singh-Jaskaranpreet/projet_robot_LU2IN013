
class AdaptateurVF:
    def __init__(self,vehicule):
        self.vehicule=vehicule

    def gerer_mouvements(self,mouv):
        if isinstance(mouv,tuple):
            if mouv[0] > 0 and mouv[1] > 0:
                if mouv[0]==mouv[1]:
                    self.vehicule.set_motor_dps("gauche_droite", mouv[0])
                else:
                    self.vehicule.set_motor_dps("gauche",mouv[0])
                    self.vehicule.set_motor_dps("droite",mouv[1])
            elif mouv[0] > 0 and mouv[1] == 0:
                self.vehicule.set_motor_dps("gauche",mouv[0])
            elif mouv[1] > 0 and mouv[0] == 0:
                self.vehicule.set_motor_dps("droite",mouv[1])
            
                

        if isinstance(mouv,str):
            
            if mouv == "carr":
                # Créer une séquence de stratégies et la démarrer
                print("le vehicule fait un carre")
                #self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
                #self.sequence.start(self.vehicule)


            if mouv == "acc":
                # Créer une séquence de stratégies et la démarrer
                print("le vehicule accelere et s'arrte devant un obstacle")
                #self.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy(self.vehicule)])
                #self.sequence.start(self.vehicule)
    
    def distance_parcouru(self,vit,temps):
        position = self.vehicule.get_motor_position()
        distance_gauche = ( position[0] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        distance_droite = ( position[1] / 360 ) * ( self.vehicule.WHEEL_CIRCUMFERENCE / 1000 )
        self.vehicule.offset_motor_encode(3,self.read_encoders())
        return (distance_droite + distance_gauche) / 2