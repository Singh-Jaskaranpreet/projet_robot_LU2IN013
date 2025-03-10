
class AdaptateurVF:
    def __init__(self,vehicule):
        self.vehicule=vehicule

    def gerer_mouvements(self,mouv):
        if isinstance(mouv,tuple):
            if mouv[0] > 0 and mouv[1] > 0:
                if mouv[0]==mouv[1]:
                    self.vehicule.set_motor_dps(3, mouv[0])
                else:
                    self.vehicule.set_motor_dps(1,mouv[0])
                    self.vehicule.set_motor_dps(2,mouv[1])
            elif mouv[0] > 0 and mouv[1] == 0:
                self.vehicule.set_motor_dps(1,mouv[0])
            elif mouv[1] > 0 and mouv[0] == 0:
                self.vehicule.set_motor_dps(2,mouv[1])
            
                

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

    def distance_parcouru(self):
        rg = ( self.vehicule.get_motor_position()[0] / 360 ) * WHEEL_CIRCUMFERENCE
        rd = ( self.vehicule.get_motor_position()[1] / 360 ) * WHEEL_CIRCUMFERENCE

        offset_motor_encode(3,self.vehicule.read_encoders()[0])

        if rd == rg :
            return rd * 1000


    