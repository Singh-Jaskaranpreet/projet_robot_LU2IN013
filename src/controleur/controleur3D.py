from src.controleur.strategy import *
from ursina import *


class Controleur3D:
    def __init__(self,Adaptateur):
        self.adaptateur = Adaptateur
        self.last_t_press = 0  # Temps du dernier appui sur "T"
        self.debounce_delay = 0.1  # Délai minimal en secondes (0.5s ici)

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
            camera.world_position = (self.adaptateur.vehicule.p_centre[1], 50, 0)
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

        if held_keys ['w']:
            camera.x += camera.forward[0]
            camera.z += camera.forward[2]
        elif held_keys ['s']:
            camera.x -= camera.forward[0]
            camera.z -= camera.forward[2]
        if held_keys ['z']:
            camera.position += camera.forward
        elif held_keys ['x']:
            camera.position -= camera.forward
        if held_keys ['a']:
            camera.position -= camera.right
        elif held_keys ['d']:
            camera.position += camera.right
        if held_keys ['q']:
            camera.rotation_y -= 1
        elif held_keys ['e']:
            camera.rotation_y += 1

        if held_keys ['c']:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.adaptateur.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.adaptateur.sequence.start(self.adaptateur)
        #    print("                                                            ", end = "\r")
        #    print("Stratégie séquentielle activée")

    def executer_strategie(self, seq = None):
        """
        Exécute la stratégie de contrôle.
        """
        if seq  == None:
            if self.adaptateur.sequence:  # Si une séquence est définie
                if self.adaptateur.vehicule.environnement.collision():  # Vérifier s'il y a une collision
                    print("                                                            ", end = "\r")
                    print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                    self.adaptateur.sequence = None  # Arrêter la stratégie
                    self.adaptateur.vehicule.vit_Rd = 0
                    self.adaptateur.vehicule.vit_Rg = 0
                elif not self.adaptateur.sequence.stop(self.adaptateur):  # Si la séquence n'est pas terminée
                    self.adaptateur.sequence.step(self.adaptateur)  # Passer à l'étape suivante
                else:  # Si la séquence est terminée
                    self.adaptateur.sequence = None  # Réinitialiser la séquence
        else:
            if seq:  # Si une séquence est définie
                if self.adaptateur.vehicule.environnement.collision():  # Vérifier s'il y a une collision
                    print("                                                            ", end = "\r")
                    print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                    seq = None  # Arrêter la stratégie
                    self.adaptateur.vehicule.vit_Rd = 0
                    self.adaptateur.vehicule.vit_Rg = 0
                elif not seq.stop(self.adaptateur):  # Si la séquence n'est pas terminée
                    seq.step(self.adaptateur)  # Passer à l'étape suivante
                else:  # Si la séquence est terminée
                    seq = None  # Réinitialiser la séquence