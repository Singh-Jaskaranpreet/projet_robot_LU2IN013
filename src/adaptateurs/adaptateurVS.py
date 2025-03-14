import pygame
import time
import sys
from src.strategy import *
from src.vehiculeF.config import *
import math

class AdaptateurVS:
    def __init__(self, vehicule):
        self.vehicule = vehicule
        self.sequence = None
        self.last_t_press = 0  # Temps du dernier appui sur "T"
        self.debounce_delay = 0.5  # Délai minimal en secondes (0.5s ici)

    def gerer_mouvements(self,mouv):
        if isinstance(mouv,tuple):
            #on convertit les degres par seconde en m/s
            mouv = (math.radians(mouv[0])*(WHEEL_DIAMETER/2),math.radians(mouv[1])*(WHEEL_DIAMETER/2))
            self.vehicule.set_vrg(mouv[0])
            self.vehicule.set_vrd(mouv[1])


        if isinstance(mouv,str):
            if mouv == "rest":
                self.vehicule.environnement.restart()

            if mouv == "carr":
                # Créer une séquence de stratégies et la démarrer
                self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
                self.sequence.start(self.vehicule)


            if mouv == "acc":
                # Créer une séquence de stratégies et la démarrer
                self.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy(self.vehicule)])
                self.sequence.start(self.vehicule)

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Augmenter la vitesse de la roue droite
            self.vehicule.set_vrd(self.vehicule.vit_Rd +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues droite, vroum vroum", end ="\r")

        elif keys[pygame.K_UP]:  # Ralentir la roue droite
            self.vehicule.set_vrd(self.vehicule.vit_Rd -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues droite, tic... tic...", end ="\r")

        if keys[pygame.K_LEFT]:  # Augmenter la vitesse de la roue gauche
            self.vehicule.set_vrg(self.vehicule.vit_Rg +1)
        #    print("                                                       ", end ="\r")
        #    print("on accelere la roues gauche, vroum vroum", end ="\r")

        elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
            self.vehicule.set_vrg(self.vehicule.vit_Rg -1)
        #    print("                                                       ", end ="\r")
        #    print("on ralentie la roues gauche, tic... tic...", end ="\r")
            
        elif keys[pygame.K_f]:
            self.vehicule.freiner(0.5)
        #    print("                                                       ", end ="\r")
        #    print("le vehicule freine, Pschhh", end ="\r")

        if keys[pygame.K_r]:
            self.vehicule.environnement.restart()
        #    print("                                                       ", end ="\r")
        #    print("oh la la on retourne à zero", end ="\r")

        if keys[pygame.K_s]:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.sequence.start(self.vehicule)
        #    print("                                                            ", end = "\r")
        #    print("Stratégie séquentielle activée")


        if keys[pygame.K_p]:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([TournerAngleStrategy(360), TournerAngleStrategy(-360), AvancerDroitStrategy(0.12)])
            self.sequence.start(self.vehicule)

        if keys[pygame.K_m]:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy(self.vehicule)])
            self.sequence.start(self.vehicule)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")

        if keys[pygame.K_t]:
                now = time.time()
                if now - self.last_t_press >= self.debounce_delay:
                    self.vehicule.environnement.basculer_tracage()
                    print("Tracé activé" if self.vehicule.environnement.trace_active else "Tracé désactivé")
                    self.last_t_press = now

        if keys[pygame.K_y]:
            self.vehicule.environnement.effacer_ligne()
            print("Ligne effacée.")

        if keys[pygame.K_b]:
            self.vehicule.environnement.asuivre_act = True
            self.sequence = StrategieSequence([SuivreObjetStrategy()])
            self.sequence.start(self.vehicule)

    def gerer_affichage(self):
        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Une touche a été pressée
                    attente = False  # On sort de la boucle et commence la simulation

    """def executer_strategie(self):
        if self.sequence:  # Si une séquence est définie
            if self.vehicule.environnement.collision():  # Vérifier s'il y a une collision
                print("                                                            ", end = "\r")
                print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                self.sequence = None  # Arrêter la stratégie
                self.vehicule.vit_Rd = 0
                self.vehicule.vit_Rg = 0
            elif not self.sequence.stop(self.vehicule):  # Si la séquence n'est pas terminée
                self.sequence.step(self.vehicule)  # Passer à l'étape suivante
            else:  # Si la séquence est terminée
                self.sequence = None  # Réinitialiser la séquence"""