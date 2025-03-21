from src.controleur.strategy import *
from ursina import *


class Controleur3D:
    def __init__(self,Adaptateur):
        self.adaptateur = Adaptateur
        self.last_t_press = 0  # Temps du dernier appui sur "T"
        self.debounce_delay = 0.5  # Délai minimal en secondes (0.5s ici)

    def gerer_evenements(self):
        """
        Gère les événements clavier pour contrôler le robot.
        :return None
        """

        if held_keys['right arrow']:  # Augmenter la vitesse de la roue droite
            self.adaptateur.vehicule.set_vrd(self.adaptateur.vehicule.vit_Rd +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues droite, vroum vroum", end ="\r")

        elif held_keys ['up arrow']:  # Ralentir la roue droite
            self.adaptateur.vehicule.set_vrd(self.adaptateur.vehicule.vit_Rd -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues droite, tic... tic...", end ="\r")

        if held_keys ['left arrow']:  # Augmenter la vitesse de la roue gauche
            self.adaptateur.vehicule.set_vrg(self.adaptateur.vehicule.vit_Rg +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues gauche, vroum vroum", end ="\r")

        elif held_keys ['down arrow']:  # Ralentir la roue gauche
            self.adaptateur.vehicule.set_vrg(self.adaptateur.vehicule.vit_Rg -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues gauche, tic... tic...", end ="\r")
            
        #elif held_keys ['f']:
        #    self.adaptateur.vehicule.freiner(0.5)
        #    print("                                                       ", end ="\r")
        #    print("le vehicule freine, Pschhh", end ="\r")

        if held_keys ['r']:
            self.adaptateur.vehicule.environnement.restart()
            camera.world_position = (self.adaptateur.vehicule.p_centre[0], 5, self.adaptateur.vehicule.p_centre[1]-20)
            camera.world_rotation_y = 0
        #    print("                                                       ", end ="\r")
        #    print("oh la la on retourne à zero", end ="\r")

        if held_keys ['s']:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.adaptateur.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.adaptateur.sequence.start(self.adaptateur)
        #    print("                                                            ", end = "\r")
        #    print("Stratégie séquentielle activée")

        if held_keys ['m']:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.adaptateur.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy()])
            self.adaptateur.sequence.start(self.adaptateur)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")

