import pygame
import time
import sys
from src.strategy import *
import math
from src.robot_général import Robot
from pygame._sdl2 import Window, Renderer
from src.robot_simulé.outils.camera import CameraView

class AdaptateurRS(Robot):
    def __init__(self, vehicule, mode):
        self.vehicule = vehicule
        self.sequence = None
        self.last_t_press = 0  # Temps du dernier appui sur "T"
        self.debounce_delay = 0.5  # Délai minimal en secondes (0.5s ici)
        self.mode = mode  # On stocke le mode (1, 2 ou 3)
        self.camera_active = False  # Ajout d'une variable pour suivre l'état de la caméra
        self.camera_window = None
        self.camera_renderer = None
        self.camera_view = None

    def gerer_evenements(self, param1 = None, param2 = None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or param1 == 'vrd':  # Augmenter la vitesse de la roue droite
            if param2 != None:
                self.vehicule.set_vrd(param2)
            else:
                self.vehicule.set_vrd(self.vehicule.vit_Rd +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues droite, vroum vroum", end ="\r")

        elif keys[pygame.K_UP]:  # Ralentir la roue droite
            self.vehicule.set_vrd(self.vehicule.vit_Rd -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues droite, tic... tic...", end ="\r")

        if keys[pygame.K_LEFT] or param1 == 'vrg':  # Augmenter la vitesse de la roue gauche
            if param2 != None:
                self.vehicule.set_vrg(param2)
            else:
                self.vehicule.set_vrg(self.vehicule.vit_Rg +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues gauche, vroum vroum", end ="\r")

        elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
            self.vehicule.set_vrg(self.vehicule.vit_Rg -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues gauche, tic... tic...", end ="\r")
            
        elif keys[pygame.K_f] or param1 == 'freiner':
            if param2 != None:
                self.vehicule.freiner(param2)
            else:
                self.vehicule.freiner(0.5)
        #    print("                                                       ", end ="\r")
        #    print("le vehicule freine, Pschhh", end ="\r")

        if keys[pygame.K_r] or param1 == 'restart':
            self.vehicule.environnement.restart()
        #    print("                                                       ", end ="\r")
        #    print("oh la la on retourne à zero", end ="\r")

        if keys[pygame.K_s] or param1 == 'carre':  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.sequence.start(self.vehicule)
        #    print("                                                            ", end = "\r")
        #    print("Stratégie séquentielle activée")

        if keys[pygame.K_m] or param1 == 'mur':  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy()])
            self.sequence.start(self.vehicule)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")

        if keys[pygame.K_t]:
                now = time.time()
                if now - self.last_t_press >= self.debounce_delay:
                    self.vehicule.environnement.basculer_tracage()
                    print("                                                            ", end = "\r")
                    print("Tracé activé" if self.vehicule.environnement.trace_active else "Tracé désactivé")
                    self.last_t_press = now

        if keys[pygame.K_y]:
            self.vehicule.environnement.effacer_ligne()
            print("                                                            ", end = "\r")
            print("Ligne effacée.")

        if keys[pygame.K_b] or param1 == 'balise':
            print("la startegy pour suivre un objet n'est pas encore fonctionnelle merci de pateinter jusqu'à la prochaine mise à jour")

            return
            now = time.time()
            if now - self.last_t_press >= self.debounce_delay:
                self.vehicule.environnement.asuivre_act = not self.vehicule.environnement.asuivre_act
                self.last_t_press = now
                if self.vehicule.environnement.asuivre_act:
                    print("Activation du suivi de balise")
                    self.sequence = SuivreObjetStrategy()  # Utilisation correcte de `self`
                    self.sequence.start(self.vehicule)
                else:
                    print("Désactivation du suivi de balise")
                    self.sequence = None  # Arrêt de la stratégie

        # Activer la caméra en appuyant sur "D"
        if self.mode == 2:
            if keys[pygame.K_d] and not self.camera_active:
                self.camera_active = True
                self.camera_window = Window("Vue Caméra", size=(640, 480))
                self.camera_renderer = Renderer(self.camera_window)
                self.camera_view = CameraView(self.vehicule.environnement, self, 640, 480, renderer=self.camera_renderer)
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
                    self.vehicule.servo_rotate(self.vehicule.angle_servo + 1)
            if keys[pygame.K_i] and self.camera_active:
                    self.vehicule.servo_rotate(self.vehicule.angle_servo - 1)
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
   
    def avancer(self,valeur):
        self.vehicule.set_vrd(valeur)
        self.vehicule.set_vrg(valeur)

    def arreter(self):
        self.vehicule.set_vrd(0)
        self.vehicule.set_vrg(0)

    def v_roue_gauche(self,valeur):
        self.vehicule.set_vrg(valeur)

    def v_roue_droite(self,valeur):
        self.vehicule.set_vrd(valeur)

    def distance_parcouru(self,vit):
        return abs(round(0.003*(abs((abs(vit)+abs(vit))/2)),3) * self.get_temps())
    
    def get_distance(self):
        return self.vehicule.infrarouge.mesurer_distance_obstacle(self.vehicule)

    def get_temps(self):
        return self.vehicule.environnement.temps.get_temps_ecoule()

    def get_essieux(self):
        return self.vehicule.essieux
    
    def get_centre(self):
        return self.vehicule.p_centre

    def get_vitesse_Rg(self):
        return self.vehicule.vit_Rg

    def get_vitesse_Rd(self):
        return self.vehicule.vit_Rd

    def reset(self):
        self.v_roue_gauche(0)
        self.v_roue_droite(0)

    def v_angulaire(self):
        return self.distance_parcouru() / ((self.get_vitesse_Rd + self.get_vitesse_Rg)/2)
    
    def get_angle(self):
        pass
    
    def faire_carre(self):
        self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
        self.sequence.start(self.vehicule)
        

