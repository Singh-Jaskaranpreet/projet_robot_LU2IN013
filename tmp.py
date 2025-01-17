#super class, cree 3 class, et class robot
class Véhicule:
    
    def __init__(self, nom : str, x: float=0, y : float=0, vitesse : float =1, nb_roues=2):
        self.nom = nom
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.nb_roues = nb_roues
#faire class    
#    def camera(self):
#        pass
    
#    def capteur_distance(self):
#        pass
    
#    def accelerometre(self):
#        pass
    
    def deplacer(self,x , y):
        while(self.x < x and self.y < y):
            x+=self.vitesse
            y+=self.vitesse



        
    """ 
    def acceleration(self, acc):
         self.vitesse += acc 
    
    def deceleration(self, red):
         self.vitesse -= red
    """

    def arret(self):
        self.vitesse = 0
    
    # def bouger(self):
    #   pass

    def get_nom(self):
        return self.nom
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_vitesse(self):
        return self.vitesse
    