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


def faire_carre(vehicule, temps, screen, couleur_vehicule, couleur_texte, environnement):
    """ Automatiser le déplacement du véhicule en carré avec plus de précision """
    cote = 100  # Longueur du côté du carré
    vitesse = 50  # Vitesse du véhicule

    for _ in range(4):
        distance_parcourue = 0

        # 🔹 Avancer précisément de "cote" pixels
        while distance_parcourue < cote:
            vehicule.accelerer(vitesse)
            dt = temps.get_temps_ecoule()
            vehicule.bouger(dt)
            distance_parcourue += vitesse * dt

            # 🔸 Vérification pour ne pas dépasser la distance
            if distance_parcourue > cote:
                vehicule.p_centre[0] -= (distance_parcourue - cote) * math.cos(math.radians(vehicule.angle))
                vehicule.p_centre[1] -= (distance_parcourue - cote) * math.sin(math.radians(vehicule.angle))
                break

            afficher(screen, vehicule, couleur_vehicule, couleur_texte, environnement.objects)
            time.sleep(0.05)  # Pause pour affichage progressif

        vehicule.freiner(vitesse)

        # 🔹 Tourner précisément de 90°
        angle_initial = vehicule.angle
        while abs(vehicule.angle - angle_initial) < 90:
            dt = temps.get_temps_ecoule()
            vehicule.tourner("gauche", dt)

            # 🔸 Vérification pour ne pas dépasser l'angle
            if abs(vehicule.angle - angle_initial) > 90:
                vehicule.angle = (angle_initial + 90) % 360
                break

            afficher(screen, vehicule, couleur_vehicule, couleur_texte, environnement.objects)
            time.sleep(0.05)  # Pause pour affichage progressif
        
        print(vehicule.p_centre)
        
        # 🔹 Arrondir les positions pour éviter les erreurs de flottants
        vehicule.p_centre[0] = round(vehicule.p_centre[0], 2)
        vehicule.p_centre[1] = round(vehicule.p_centre[1], 2)
        vehicule.angle = round(vehicule.angle) % 360    

    vehicule.vit_Rg = 0
    vehicule.vit_Rd = 0

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
        print("                                                       ", end ="\r")
        print("je tourne à droite, Tick... Tick... Tick...", end ="\r")

    elif keys[pygame.K_LEFT]:
        environnement.vehicule.tourner("gauche",temps.get_temps_ecoule())
        print("                                                       ", end ="\r")
        print("je tourne à gauche, Tick... Tick... Tick...", end ="\r")
 
    if keys[pygame.K_UP]:
        environnement.vehicule.accelerer(0.5) 
        print("                                                       ", end ="\r")      
        print("le vehicule accèlere, Vroum Vroum", end ="\r")

    elif keys[pygame.K_DOWN]:
        environnement.vehicule.reculer(0.5)
        print("                                                       ", end ="\r")
        print("le vehicule recule, Bip... Bip... ", end ="\r")

    elif keys[pygame.K_f]:
        environnement.vehicule.freiner(0.5)
        print("                                                       ", end ="\r")
        print("le vehicule freine, Pschhh", end ="\r")

    if keys[pygame.K_r]:
        environnement.vehicule.restart()
        print("                                                       ", end ="\r")
        print("oh la la on retourne à zero", end ="\r")

    if keys[pygame.K_c]:  
        faire_carre(environnement.vehicule, temps, screen, ROUGE, NOIR, environnement)
        print("                                                       ", end ="\r")
        print("le vehicule fait un carré", end ="\r")



    environnement.vehicule.bouger(temps.get_temps_ecoule())
    environnement.collision(0)
    temps.demarrer()
    environnement.rester_dans_limites()
    tourner = ""

    # Affichage
    afficher(screen, environnement.vehicule, ROUGE, NOIR, environnement.objects)
    clock.tick(60)

temps.arreter()