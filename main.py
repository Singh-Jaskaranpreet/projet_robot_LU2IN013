from src.robot_réel import VehiculeR
import sys
from src.robot_simulé import *
from src.robot_simulé.affichage3D import Affichage3D
from src.adaptateurs import AdaptateurRR,AdaptateurRS
from src.controleur import Controleur
import time
import random as r
import threading

#On récupère les arguments passés en ligne de commande
global param1
global param2

if len(sys.argv) == 3:
    try:
        param1 = float(sys.argv[1])
        param2 = float(sys.argv[2])
    except ValueError:
        print("Les paramètres doivent être des nombres.")
        sys.exit(1)

elif len(sys.argv) == 2:
    param1 = sys.argv[1]
    param2 = None

    assert isinstance(param1, str), "Le paramètre doit être une chaîne de caractères."

else:
    print("Usage : python3 main.py <number1> <number2> ou python3 main.py <string>")
    sys.exit(1)



#Création de l'environnement et d'un véhicule et des adaptateurs
robot = VehiculeR(0, 0, 0)
environnement = Environnement()
adapVS = AdaptateurRS(environnement.vehicule)
adapVR = AdaptateurRR(robot)
controleur = Controleur(adapVS,adapVR)

print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")

# Démarrer l'horloge du véhicule une seule fois
environnement.temps.demarrer()
while True:
    try:
        k = int(input("Votre choix : "))
        if k in [1, 2 ,3]:
            break
        print("Mode non implémenté, veuillez choisir 1 ou 2 ou 3")
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

if k==3:
        
    aff3d=Affichage3D(environnement.vehicule)
    
    aff3d.afficher(environnement.objects,environnement)


     
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
        
        # Gestion des contrôles par l'utilisateur
        if param2 is not None:
            adapVS.v_roue_gauche(param1)
            adapVS.v_roue_droite(param2)
            adapVR.v_roue_gauche(param1)
            adapVR.v_roue_droite(param2)
                                                                                                                                                                                                                
        else :
            if param1 =="carre":
                adapVS.faire_carre()
                controleur.executer_strategie()
                
                #adapVR.faire_carre()
                
                

        controleur.adapVS.gerer_evenements()
        controleur.executer_strategie()

        environnement.bouger()
        environnement.temps.demarrer()
        environnement.rester_dans_limites()

        # Affichage
        affichage.afficher(environnement.objects, environnement)

    
        
    # Pause pour limiter la fréquence d'itération (environ 60 itérations/s)
    time.sleep(1/60)

    environnement.temps.arreter()