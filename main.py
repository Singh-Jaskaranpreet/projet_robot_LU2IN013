import pygame
import sys
from src.modele import Environnement,Vehicule, Environnement3D
from src.affichage import Affichage, Affichage3D
from src.controleur import Controleur
import src.controleur.lcm as lcm
import time
import random as r
import threading


#temps Création de l'environnement et d'un véhicule
environnement = Environnement()
controleur = Controleur(environnement.vehicule)

print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")
k = int(input("Votre choix :"))

# Démarrer l'horloge du véhicule une seule fois
environnement.temps.demarrer()
if k==1 :
        # Initialiser last_print avant la boucle
        last_print = time.time()

        # Lancer la lecture des commandes dans un thread séparé
        threading.Thread(target=lcm.lire_commandes, args=(environnement,), daemon=True).start()

if k==2:
        affichage = Affichage(1200,800)

        # Affiche l'écran d'instructions avant de commencer
        affichage.afficher_instructions()
        # Attendre que l'utilisateur appuie sur une touche pour commencer
        controleur.gerer_affichage()

if k == 3:
    # Crée une seule instance de ShowBase via Affichage3D
    affichage3d = Affichage3D()       
    # Passe cette instance à l'environnement 3D
    environnement3d = Environnement3D(affichage3d)
    # On suppose ici que l'environnement3d gère déjà la création de ses véhicules
    controleur = Controleur(environnement3d.vehicules)

    # Définition d'une tâche pour mettre à jour la simulation dans Panda3D
    def update_simulation(task):
        
        return task.cont

    affichage3d.taskMgr.add(update_simulation, "UpdateSimulation")
    affichage3d.run()  # Lance la boucle principale de Panda3D

x=0
while True :
    if k==1 :
        # Exécuter la stratégie en cours (si applicable)
        controleur.executer_strategie()

        # Mettre à jour la simulation
        environnement.bouger()
        environnement.rester_dans_limites()

        # Affichage des infos de simulation toutes les 1 seconde
        # seulement si l'utilisateur n'est pas en train de taper une commande
        if  time.time() - last_print > 2:
            last_print = time.time()
            lcm.info(environnement)


    if k==2:
        
        while x > 8 :
            affichage.couleurs[3]=r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)
            x=0
        x+=1
        environnement.temps.set_time_scale(1)
        controleur.executer_strategie()
        # Gestion des contrôles par l'utilisateur
        controleur.gerer_evenements()

        environnement.bouger()
        environnement.temps.demarrer()
        environnement.rester_dans_limites()

        # Affichage
        affichage.afficher(environnement.objects, environnement)

    
        
    # Pause pour limiter la fréquence d'itération (environ 60 itérations/s)
    time.sleep(1/60)

environnement.temps.arreter()