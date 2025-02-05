import time
from datetime import timedelta
import threading

class Horloge:
    def __init__(self):
        self.start_time = None
        self.running = False

    def demarrer(self):
        """Démarre l'horloge."""
        self.start_time = time.time()
        self.running = True
        threading.Thread(target=self._afficher_temps, daemon=True).start()

    def _afficher_temps(self):
        """Affiche le temps écoulé en temps réel."""
        while self.running:
            elapsed_time = time.time() - self.start_time
            formatted_time = timedelta(seconds=elapsed_time)
            time.sleep(1)

    def arreter(self):
        """Arrête l'horloge et retourne le temps total écoulé."""
        self.running = False
        elapsed_time = time.time() - self.start_time
        formatted_time = timedelta(seconds=elapsed_time)
        return formatted_time.total_seconds()

    def get_temps_ecoule(self):
        """Retourne le temps écoulé sous forme de chaîne formatée."""
        if self.start_time is None:
            return "00:00:00"
        elapsed_time = time.time() - self.start_time
        return timedelta(seconds=elapsed_time).total_seconds()