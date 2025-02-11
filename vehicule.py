import infrarouge
import horloge

# Classe Véhicule
class Vehicule:

    def __init__(self, nom, p_centre,empattement,essieux, angle = 0):
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
        self.temps = horloge.Horloge()
        self.infrarouge = infrarouge.Infrarouge()
    
    def accelerer(self, val):
        self.vit_Rg = max(0,min(150,self.vit_Rg+val))
        self.vit_Rd = max(min(150,self.vit_Rd+val))
    
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
        self.vit_Rd = max(-100, min(x, 150))

    def set_vrg(self, x):
        self.vit_Rg = max(-100, min(x, 150))

    def acr_Rg(self, val):
        self.vit_Rg = max(-100,min(150,self.vit_Rg+val))

    def acr_Rd(self, val):
        self.vit_Rd = max(-100,min(150,self.vit_Rd+val))
