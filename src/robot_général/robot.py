from abc import ABC, abstractmethod

class Robot(ABC):
    @abstractmethod
    def avancer(self,valeur):
        """
        Fait avancer le robot de valeur
        """
        pass

    @abstractmethod
    def arreter(self):
        """
        Arrete le robot
        """
        pass
    
    @abstractmethod
    def v_roue_gauche(self,valeur):
        """
        Donne une vitesse à la roues gauche
        """
        pass
    
    @abstractmethod
    def v_roue_droite(self,valeur):
        """
        Donne une vitesse à la roues droite
        """
        pass
    
    @abstractmethod
    def distance_parcouru(self):
        """
        Donne la distance parcouru par le robot
        """
        pass

    @abstractmethod
    def get_distance(self):
        """
        Retourne la distance par rapport à un obstacle devant lui
        """
        pass

    @abstractmethod
    def get_temps(self):
        """
        Retourne le temps écoulé
        """
        pass

    @abstractmethod
    def get_essieux(self):
        """
        Retourne la distance entre les deux roues
        """
        pass
    
    @abstractmethod
    def get_vitesse_Rg(self):
        """
        Retourne la vitesse de la roue gauche
        """
        pass

    @abstractmethod
    def get_vitesse_Rd(self):
        """
        Retourne la vitesse de la roue droite
        """
        pass

    @abstractmethod
    def get_angle(self):
        """
        Retourne l'angle du robot
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset le robot
        """
        pass

    @abstractmethod
    def faire_carre(self):
        """
        Fait un carré
        """
        pass

    @abstractmethod
    def v_angulaire(self):
        """
        Donne une vitesse angulaire
        """
        pass
    

