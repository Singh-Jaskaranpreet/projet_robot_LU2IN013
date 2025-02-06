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
environnement = Environnement(LARGEUR, HAUTEUR)
vehicule = Vehicule("Robot",0 ,0 , [200, HAUTEUR // 2], 50)


obs=[pygame.Rect(randint(400, 900), randint(0,HAUTEUR//2), randint(10,100), randint(200,HAUTEUR//2))]
temps = Horloge()


def rester_dans_limites(vehicule):
        """ Empêche le véhicule de sortir de l'écran et arrête sa vitesse. """
        for point in vehicule.position_des_roues(vehicule.p_centre):
            if point[0] < 10 or point[0] > LARGEUR - 10  or point[1] < 10 or point[1] > HAUTEUR - 10 :
                vehicule.arret()
            if point[0] < 0 or point[0] > LARGEUR   or point[1] < 0 or point[1] > HAUTEUR :
                vehicule.restart()
        return


# Afficher l'écran d'instructions avant de commencer
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
    vehicule.mesurer_distance_obstacle(environnement, obs)
    
    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        vehicule.tourner("droite", environnement, obs)

    elif keys[pygame.K_LEFT]:
        vehicule.tourner("gauche", environnement, obs)
            
    if keys[pygame.K_UP]:
        vehicule.acceleration(0.5)       
            
    elif keys[pygame.K_DOWN]:
        vehicule.deceleration(0.5)
            
    if keys[pygame.K_SPACE]:
        vehicule.arret()
        
    if keys[pygame.K_r]:
        vehicule.restart()

    vehicule.bouger(environnement, obs, temps.get_temps_ecoule())
    temps.demarrer()
    rester_dans_limites(vehicule)


    # Affichage
    screen.fill(BLANC)
    afficher(screen, vehicule, ROUGE, NOIR, obs)
    pygame.display.flip()
    clock.tick(60)

temps.arreter()