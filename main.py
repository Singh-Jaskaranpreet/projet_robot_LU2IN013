from src.modele import Environnement
from src.affichage import Affichage
from src.controleur import Controleur
from src.vehiculeF import VehiculeF
from src.adaptateurs import AdaptateurVF,AdaptateurVS
import src.controleur.controleur as controleur
import time
import random as r
import threading


#temps Création de l'environnement et d'un véhicule et des adaptateurs
robot = VehiculeF(0, 0, 0)
environnement = Environnement()
adapVS = AdaptateurVS(environnement.vehicule)
adapVF = AdaptateurVF(robot)
controleur = Controleur(adapVS,adapVF)

print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")

# Démarrer l'horloge du véhicule une seule fois
environnement.temps.demarrer()
while True:
    try:
        k = int(input("Votre choix : "))
        if k in [1, 2]:
            break
        print("Mode non implémenté, veuillez choisir 1 ou 2.")
    except ValueError:
        print("Entrée invalide, veuillez saisir un nombre.")

if k==1 :
        # Initialiser last_print avant la boucle
        last_print = time.time()

        # Lancer la lecture des commandes dans un thread séparé
        threading.Thread(target=controleur.lire_commandes, daemon=True).start()

if k==2:
        affichage = Affichage(1200,800)

        # Affiche l'écran d'instructions avant de commencer
        #affichage.afficher_instructions()
        # Attendre que l'utilisateur appuie sur une touche pour commencer
        #controleur.gerer_affichage()
        controleur.choix = False
        threading.Thread(target=controleur.lire_commandes, daemon=True).start()

     
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
            


    if k==2:
        
        while x > 8 :
            affichage.couleurs[3]=r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)
            x=0
        x+=1
        environnement.temps.set_time_scale(1)
        controleur.executer_strategie()
        # Gestion des contrôles par l'utilisateur
        controleur.adapVS.gerer_evenements()

        environnement.bouger()
        environnement.temps.demarrer()
        environnement.rester_dans_limites()

        # Affichage
        affichage.afficher(environnement.objects, environnement)

    
        
    # Pause pour limiter la fréquence d'itération (environ 60 itérations/s)
    time.sleep(1/60)

environnement.temps.arreter()