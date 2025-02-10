import pygame
import environnement
import sys

class Controleur:
    def __init__(self, vehicule, environnement):
        self.vehicule = vehicule
        self.environnement = environnement

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:  # Augmenter la vitesse de la roue droite
            self.vehicule.vit_Rd = min(150, self.vehicule.vit_Rd + 1)
         
        elif keys[pygame.K_UP]:  # Ralentir la roue droite
            self.vehicule.vit_Rd = max(-50, self.vehicule.vit_Rd - 1)

        if keys[pygame.K_LEFT]:  # Augmenter la vitesse de la roue gauche
            self.vehicule.vit_Rg = min(150, self.vehicule.vit_Rg + 1)

        elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
            self.vehicule.vit_Rg = max(-50, self.vehicule.vit_Rg - 1)

        elif keys[pygame.K_f]:
            self.vehicule.freiner(0.5)
            print("                                                       ", end ="\r")
            print("le vehicule freine, Pschhh", end ="\r")

        if keys[pygame.K_r]:
            self.vehicule.restart()
            print("                                                       ", end ="\r")
            print("oh la la on retourne à zero", end ="\r")

    def gerer_affichage(self):
        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Une touche a été pressée
                    attente = False  # On sort de la boucle et commence la simulation
