import pygame
import time
import sys
from ..strategy import *

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
            print("                                                       ", end ="\r")
            print("on accelere la roues droite, vroum vroum", end ="\r")

        elif keys[pygame.K_UP]:  # Ralentir la roue droite
            self.vehicule.set_vrd(self.vehicule.vit_Rd -1)
            print("                                                       ", end ="\r")
            print("on ralentie la roues droite, tic... tic...", end ="\r")

        if keys[pygame.K_LEFT]:  # Augmenter la vitesse de la roue gauche
            self.vehicule.set_vrg(self.vehicule.vit_Rg +1)
            print("                                                       ", end ="\r")
            print("on accelere la roues gauche, vroum vroum", end ="\r")

        elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
            self.vehicule.set_vrg(self.vehicule.vit_Rg -1)
            print("                                                       ", end ="\r")
            print("on ralentie la roues gauche, tic... tic...", end ="\r")
            
        elif keys[pygame.K_f]:
            self.vehicule.freiner(0.5)
            print("                                                       ", end ="\r")
            print("le vehicule freine, Pschhh", end ="\r")

        if keys[pygame.K_r]:
            self.vehicule.environnement.restart()
            print("                                                       ", end ="\r")
            print("oh la la on retourne à zero", end ="\r")

        if keys[pygame.K_s]:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
            self.sequence.start(self.vehicule)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")

        if keys[pygame.K_m]:  # Définir une séquence de stratégies
            # Créer une séquence de stratégies et la démarrer
            self.sequence = StrategieSequence([AccelererStrategy(), DoucementStrategy(self.vehicule)])
            self.sequence.start(self.vehicule)
            print("                                                            ", end = "\r")
            print("Stratégie séquentielle activée")