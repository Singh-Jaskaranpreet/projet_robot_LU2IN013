import time
from datetime import timedelta


class Horloge:
    def __init__(self):
        """
        Initialise l'horloge.
        :param start_time: Temps de démarrage de l'horloge
        :param running: Indique si l'horloge est en marche
        :param time_scale: Facteur de vitesse (1 = temps normal
        """
        self.start_time = None
        self.running = False
        self.time_scale = 1  # Facteur de vitesse (1 = temps normal)

    def demarrer(self):
        """
        Démarre l'horloge.
        """
        self.start_time = time.time()
        self.running = True

    def arreter(self):
        """
        Arrête l'horloge et retourne le temps total écoulé.
        """
        self.running = False
        elapsed_time = time.time() - self.start_time
        formatted_time = timedelta(seconds=elapsed_time)
        return formatted_time.total_seconds()

    def get_temps_ecoule(self):
        """
        Retourne le temps écoulé sous forme de chaîne formatée.
        """
        if self.start_time is None:
            return "00:00:00"
        elapsed_time = (time.time() - self.start_time)*self.time_scale
        return timedelta(seconds=elapsed_time).total_seconds()
    
    def set_time_scale(self, scale):
        """
        Définit le facteur de vitesse.
        :param scale: Facteur de vitesse (1 = temps normal)
        """
        if scale > 0:  # Assurez-vous que le facteur de vitesse est positif
            self.time_scale = scale
        else:
            print("Le facteur de vitesse doit être supérieur à 0.")