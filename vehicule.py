import infrarouge
import math as m

# Classe Véhicule
class Vehicule:

    def __init__(self, nom, p_centre,empattement,essieux, environnement, angle = 0,):
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
        self.infrarouge = infrarouge.Infrarouge()
    
    def accelerer(self, val):
        self.vit_Rg = max(0, min(150, self.vit_Rg+val))
        self.vit_Rd = max(0, min(150, self.vit_Rd+val))
    
    def freiner(self, val):
        if self.vit_Rg > 0:
            self.vit_Rg = max(0,self.vit_Rg-val)
        elif self.vit_Rg < 0:
            self.vit_Rg = min(0,self.vit_Rg+val)
        if self.vit_Rd > 0:
            self.vit_Rd = max(0,self.vit_Rd-val)
        elif self.vit_Rd < 0:
            self.vit_Rd = min(0,self.vit_Rd+val)

    def reculer(self, val):
        self.vit_Rg = max(-50, self.vit_Rg - val)
        self.vit_Rd = max(-50, self.vit_Rd - val)

        
    def get_distance(self, environnement):
        return self.infrarouge.mesurer_distance_obstacle(environnement)
    
    def set_vrd(self, x):
        self.vit_Rd = max(-150, min(x, 150))

    def set_vrg(self, x):
        self.vit_Rg = max(-150, min(x, 150))

    def acr_Rg(self, val):
        self.vit_Rg = max(-150,min(150,self.vit_Rg+val))

    def acr_Rd(self, val):
        self.vit_Rd = max(-150,min(150,self.vit_Rd+val))

    #Place les trois roues de la voiture
    def position_des_roues(self, point):
        hyp = self.long / m.cos(m.radians(20))
        r_Ar = [point[0] - (self.long//2) * m.cos(m.radians(self.angle)), point[1] - (self.long//2) * m.sin(m.radians(self.angle))]
        r_Avg = [r_Ar[0] + hyp * m.cos(m.radians(self.angle + 20)), r_Ar[1] + hyp * m.sin(m.radians(self.angle + 20))]
        r_Avd = [r_Ar[0] + hyp * m.cos(m.radians(self.angle - 20)), r_Ar[1] + hyp * m.sin(m.radians(self.angle - 20))]
        return [r_Ar, r_Avg, r_Avd]
