import pygame
import sys
from vehicule import *
from environnement import *
from random import *
from horloge import *
from affichage import *
import time
import math

# Initialisation de Pygame
pygame.init()

# Création de l'environnement et d'un véhicule
environnement = Environnement()

temps = Horloge()


# Affiche l'écran d'instructions avant de commencer
afficher_instructions()

# Attendre que l'utilisateur appuie sur une touche pour commencer
attente = True
while attente:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # Une touche a été pressée
            attente = False  # On sort de la boucle et commence la simulation

# Boucle principale de la simulation
clock = pygame.time.Clock()
temps.demarrer()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:  # Augmenter la vitesse de la roue droite
        environnement.vehicule.vit_Rd = min(150, environnement.vehicule.vit_Rd + 1)
         
    elif keys[pygame.K_UP]:  # Ralentir la roue droite
        environnement.vehicule.vit_Rd = max(-50, environnement.vehicule.vit_Rd - 1)

    if keys[pygame.K_LEFT]:  # Augmenter la vitesse de la roue gauche
        environnement.vehicule.vit_Rg = min(150, environnement.vehicule.vit_Rg + 1)

    elif keys[pygame.K_DOWN]:  # Ralentir la roue gauche
        environnement.vehicule.vit_Rg = max(-50, environnement.vehicule.vit_Rg - 1)

    elif keys[pygame.K_f]:
        environnement.vehicule.freiner(0.5)
        print("                                                       ", end ="\r")
        print("le vehicule freine, Pschhh", end ="\r")

    if keys[pygame.K_r]:
        environnement.vehicule.restart()
        print("                                                       ", end ="\r")
        print("oh la la on retourne à zero", end ="\r")



    environnement.vehicule.bouger(temps.get_temps_ecoule())
    collision = environnement.collision()
    la = 0
    while(collision):
        environnement.correction_apres_collision(collision)
        collision = environnement.collision()
        la=1
    if la == 1 :
        environnement.arrete()
        la=0
    temps.demarrer()
    environnement.rester_dans_limites()

    # Affichage
    afficher(screen, environnement.vehicule, ROUGE, NOIR, environnement.objects, environnement)
    clock.tick(60)

temps.arreter()