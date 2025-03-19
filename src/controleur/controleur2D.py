from src.controleur import *
import pygame
import time
import sys
from pygame._sdl2 import Window, Renderer
from src.simulation.outils.camera import CameraView
class Controleur2D:
    def __init__(self,Adaptateur,mode):
        self.adaptateur = Adaptateur
        self.last_t_press = 0  # Temps du dernier appui sur "T"
        self.debounce_delay = 0.5  # Délai minimal en secondes (0.5s ici)
        self.mode = mode  # On stocke le mode (1, 2 ou 3)
        self.camera_active = False  # Ajout d'une variable pour suivre l'état de la caméra
        self.camera_window = None
        self.camera_renderer = None
        self.camera_view = None

    def gerer_evenements(self, param1 = None, param2 = None):
        """
        Gère les événements clavier pour contrôler le robot.
        :param param1: Permet de déclencher une action sans appuyer sur une touche.
        :param param2: Permet de passer un paramètre à l'action déclenchée.
        :return None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or param1 == 'vrd':  # Augmenter la vitesse de la roue droite
            if param2 != None:
                self.adaptateur.vehicule.set_vrd(param2)
            else:
                self.adaptateur.vehicule.set_vrd(self.adaptateur.vehicule.vit_Rd +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues droite, vroum vroum", end ="\r")

        elif keys[pygame.K_UP]:  # Ralentir la roue droite
            self.adaptateur.vehicule.set_vrd(self.adaptateur.vehicule.vit_Rd -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues droite, tic... tic...", end ="\r")

        if keys[pygame.K_LEFT] or param1 == 'vrg':  # Augmenter la vitesse de la roue gauche
            if param2 != None:
                self.adaptateur.vehicule.set_vrg(param2)
            else:
                self.adaptateur.vehicule.set_vrg(self.adaptateur.vehicule.vit_Rg +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues gauche, vroum vroum", end ="\r")

        elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
            self.adaptateur.vehicule.set_vrg(self.adaptateur.vehicule.vit_Rg -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues gauche, tic... tic...", end ="\r")
            
        elif keys[pygame.K_f] or param1 == 'freiner':
            if param2 != None:
                self.adaptateur.vehicule.freiner(param2)
            else:
                self.adaptateur.vehicule.freiner(0.5)
        #    print("                                                       ", end ="\r")
        #    print("le vehicule freine, Pschhh", end ="\r")

        if keys[pygame.K_r] or param1 == 'restart':
            self.adaptateur.vehicule.environnement.restart()
        #    print("                                                       ", end ="\r")
        #    print("oh la la on retourne à zero", end ="\r")

        if keys[pygame.K_s] or param1 == 'carre':  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.adaptateur.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.adaptateur.sequence.start(self.adaptateur)
        #    print("                                                            ", end = "\r")
        #    print("Stratégie séquentielle activée")

        if keys[pygame.K_m] or param1 == 'mur':  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.adaptateur.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy()])
            self.adaptateur.sequence.start(self.adaptateur)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")

        if keys[pygame.K_t]:
                now = time.time()
                if now - self.last_t_press >= self.debounce_delay:
                    self.adaptateur.vehicule.environnement.basculer_tracage()
                    print("                                                            ", end = "\r")
                    print("Tracé activé" if self.adaptateur.vehicule.environnement.trace_active else "Tracé désactivé")
                    self.last_t_press = now

        if keys[pygame.K_y]:
            self.adaptateur.vehicule.environnement.effacer_ligne()
            print("                                                            ", end = "\r")
            print("Ligne effacée.")

        if keys[pygame.K_b] or param1 == 'balise':
            print("la startegy pour suivre un objet n'est pas encore fonctionnelle merci de pateinter jusqu'à la prochaine mise à jour")

            return
            now = time.time()
            if now - self.last_t_press >= self.debounce_delay:
                self.adaptateur.vehicule.environnement.asuivre_act = not self.adaptateur.vehicule.environnement.asuivre_act
                self.last_t_press = now
                if self.adaptateur.vehicule.environnement.asuivre_act:
                    print("Activation du suivi de balise")
                    self.sequence = SuivreObjetStrategy()  # Utilisation correcte de `self`
                    self.sequence.start(self.adaptateur.vehicule)
                else:
                    print("Désactivation du suivi de balise")
                    self.sequence = None  # Arrêt de la stratégie

        # Activer la caméra en appuyant sur "D"
        if self.mode == 2:
            if keys[pygame.K_d] and not self.camera_active:
                self.camera_active = True
                self.camera_window = Window("Vue Caméra", size=(640, 480))
                self.camera_renderer = Renderer(self.camera_window)
                self.camera_view = CameraView(self.adaptateur.vehicule.environnement, self, 640, 480, renderer=self.camera_renderer)
                print("                                                       ", end ="\r")
                print("Caméra activée, Fshiou...", end ="\r")

            if keys[pygame.K_p] and self.camera_active:
                self.camera_active = False
                self.camera_window.destroy()  # Fermer la fenêtre SDL2 proprement
                self.camera_window = None
                self.camera_renderer = None
                self.camera_view = None
                print("                                                       ", end ="\r")
                print("Caméra désactivée, Pshiou...", end ="\r")
        if self.mode == 3 or self.mode == 2:
            if keys[pygame.K_o] and self.camera_active:
                    self.adaptateur.vehicule.servo_rotate(self.adaptateur.vehicule.angle_servo + 1)
            if keys[pygame.K_i] and self.camera_active:
                    self.adaptateur.vehicule.servo_rotate(self.adaptateur.vehicule.angle_servo - 1)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()


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
