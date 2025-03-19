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
    def set_VrG(self,valeur):
        """
        Donne une vitesse à la roues gauche
        """
        pass
    
    @abstractmethod
    def set_VrD(self,valeur):
        """
        Donne une vitesse à la roues droite
        """
        pass
    
    @abstractmethod
    def get_distance_parcouru(self):
        """
        Donne la distance parcouru par le robot
        """
        pass

    @abstractmethod
    def get_distance_to_obstacle(self):
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
    def get_VrG(self):
        """
        Retourne la vitesse de la roue gauche
        """
        pass

    @abstractmethod
    def get_VrD(self):
        """
        Retourne la vitesse de la roue droite
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Reset le robot
        """
        pass

    @abstractmethod
    def get_angle_parcourueRad(self,vitesse):
        """
        Retourne l'angle parcourue lors de la rotation
        """
        omega = vitesse / self.get_essieux()
        return omega*self.get_temps()
    

