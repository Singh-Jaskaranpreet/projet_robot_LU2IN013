import pygame
import sys
from src.modele import Environnement,Vehicule
from src.affichage import Affichage
from src.controleur import Controleur
import src.controleur.lcm as lcm
import time
import random as r
import threading


#temps Création de l'environnement et d'un véhicule
environnement = Environnement()
controleur = Controleur(environnement.vehicule,environnement)

print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")
k = int(input("Votre choix :"))

# Démarrer l'horloge du véhicule une seule fois
environnement.temps.demarrer()
while k >= 3:
        if k==3:
            print("pas implémenter, veuillez choisir autre chose")
        else:
            print("la commande n'est pas reconue veuillez choiisr un nombre entre 1, 2 et 3")
        k=0
        print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")
        k = int(input("Votre choix :"))

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
        #controleur.gerer_affichage()
     
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