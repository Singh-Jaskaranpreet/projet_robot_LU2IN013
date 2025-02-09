import pygame
import sys
from vehicule import *
from environnement import *
from random import *
from horloge import *
from affichage import *

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1200, 800

# Création de l'environnement et d'un véhicule
vehicule = Vehicule("Robot",[200, 400] , 50, 50)
obs=[[(400,100),(600,100),(600,600),(400,600)]]
environnement = Environnement(LARGEUR, HAUTEUR, vehicule, obs)

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
    environnement.vehicule.mesurer_distance_obstacle(environnement)
    
    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        environnement.vehicule.tourner("droite",temps.get_temps_ecoule())

    elif keys[pygame.K_LEFT]:
        environnement.vehicule.tourner("gauche",temps.get_temps_ecoule())
            
    if keys[pygame.K_UP]:
        environnement.vehicule.accelerer(0.5)       
            
    elif keys[pygame.K_DOWN]:
        environnement.vehicule.freiner(0.5)
        
    if keys[pygame.K_r]:
        environnement.vehicule.restart()

    environnement.vehicule.bouger(temps.get_temps_ecoule())
    environnement.collision()
    temps.demarrer()
    environnement.rester_dans_limites()


    # Affichage
    afficher(screen, environnement.vehicule, ROUGE, NOIR, environnement.objects)
    clock.tick(60)

temps.arreter()