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

        if keys[pygame.K_m]:  # Définir une séquence de stratégies
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


    def distance_parcouru(self,vit,temps):
        return abs(round(0.003*(abs((abs(vit)+abs(vit))/2)),3) * temps)
    
    def get_distance(self):
        return self.vehicule.infrarouge.mesurer_distance_obstacle(self.vehicule)
    