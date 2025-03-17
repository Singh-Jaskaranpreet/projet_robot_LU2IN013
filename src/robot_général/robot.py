from abc import ABC, abstractmethod

class Robot(ABC):
    @abstractmethod
    def avancer(self,valeur):
        pass

    @abstractmethod
    def arreter(self):
        pass
    
    @abstractmethod
    def v_roue_gauche(self,valeur):
        pass
    
    @abstractmethod
    def v_roue_droite(self,valeur):
        pass
    
    @abstractmethod
    def distance_parcouru(self):
        pass

    @abstractmethod
    def get_distance(self):
        pass

    @abstractmethod
    def get_temps(self):
        pass

    @abstractmethod
    def get_essieux(self):
        pass
    
    @abstractmethod
    def get_vitesse_Rg(self):
        pass

    @abstractmethod
    def get_vitesse_Rd(self):
        pass

    @abstractmethod
    def get_angle(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def faire_carre(self):
        pass

    @abstractmethod
    def v_angulaire(self):
        pass
    

