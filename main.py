import sys
from src.simulation.environnement import Environnement
from src.affichage import Affichage3D,Affichage2D
from src.modele import AdaptateurRR,AdaptateurRS,VehiculeR
from src.controleur import Controleur3D,Controleur2D,Controleur
from src.controleur.strategy import *
import time
import random as r
import threading


#On récupère les arguments passés en ligne de commande
global param1
global param2
strategy = None

if len(sys.argv) == 3:
    try:
        param1 = int(sys.argv[1])
        param2 = int(sys.argv[2])
    except ValueError:
        print("Les paramètres doivent être des nombres.")
        sys.exit(1)

elif len(sys.argv) == 2:
    param1 = sys.argv[1]
    param2 = None

    assert isinstance(param1, str), "Le paramètre doit être une chaîne de caractères."

else:
    #print("Usage : python3 main.py <number1> <number2> ou python3 main.py <string>")
    #sys.exit(1)
    print("il est préférable de donné un argument au main")
    param1 = None
    param2 = None

#On choisi quel robot faire bouger

print("Choisir quel robot vous voulez utilisez vos choix sont:\n1- R pour le Robot Réel\n2- S pour le Robot Simulé\n")
s=''
while True:
    try:
        s = input("Votre choix : ")
        if s in ['R', 'S']:
            break #remplacer par la logique de choix
        print("Version non reconnue")
    except ValueError:
        print("Merci de choisir entre R et S")

if s=='R':
    robot = VehiculeR()
    adapRR = AdaptateurRR(robot)
    controleur = Controleur(adapRR)

    if param2 is not None:
            adapRR.v_roue_gauche(param1)
            adapRR.v_roue_droite(param2)
            param1=None
            param2=None


    else:
        if param1 == "carre":
            strategy = faire_carre(strategy, robot)
            controleur.executer_strategie(strategy)
            param1 = None
            while not strategy.stop(robot):
                controleur.executer_strategie(strategy)
                time.sleep(0.1)
            print ('on a fait un jolie carré')

        elif param1 == "mur":
            strategy = proche_mur(strategy, robot)
            controleur.executer_strategie(strategy)
            param1 = None
            while not strategy.stop(robot):
                controleur.executer_strategie(strategy)
                time.sleep(0.1)
            print('on s est rapproché du mur')

else :
    environnement = Environnement()
    print("Comment voulez vous votre Simulation:\n1-Terminal\n2-Affichage 2D\n3-Affichage 3D\n")
    while True:
        try:
            k = int(input("Votre choix : "))
            if k in [1, 2 ,3]:
                break
            print("Mode non implémenté, veuillez choisir 1 ou 2 ou 3")
        except ValueError:
            print("Entrée invalide, veuillez saisir un nombre.")
    adapRS = AdaptateurRS(environnement.vehicule)
    controleur2D = Controleur2D(adapRS,k)
    controleur3D = Controleur3D(adapRS)

    #Création du controleur
    controleur = Controleur(adapRS)

    # Démarrer l'horloge du véhicule une seule fois
    environnement.temps.demarrer()

    if k==1 :
            # Initialiser last_print avant la boucle
            last_print = time.time()

            # Lancer la lecture des commandes dans un thread séparé
            threading.Thread(target=controleur.lire_commandes, daemon=True).start()

    if k==2:
            affichage = Affichage2D(1200,800)
            #threading.Thread(target=controleur.lire_commandes, daemon=True).start()

    if k==3:
            
        aff3d=Affichage3D(environnement)
        aff3d.afficher()

    
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
                adapRS.v_roue_gauche(param1)
                adapRS.v_roue_droite(param2)
                param1=None
                param2=None

                                                                                                                                                                                                                    
            else :
                if param1 =="carre":
                    strategy = faire_carre(strategy, environnement.vehicule)
                    controleur.executer_strategie(strategy)
                    param1 = None

                elif param1 == "mur":
                    strategy = proche_mur(strategy, environnement.vehicule)
                    controleur.executer_strategie(strategy)

                    
                    
            controleur2D.gerer_evenements()
            controleur2D.executer_strategie()

            environnement.bouger()
            environnement.temps.demarrer()
            environnement.rester_dans_limites()

            if controleur2D.camera_active:
                controleur2D.camera_view.render()

            # Affichage
            affichage.afficher(environnement.objects, environnement)
        
        if k == 3 :
            environnement.temps.set_time_scale(1)
            
            # Gestion des contrôles par l'utilisateur
            if param2 is not None:
                adapRS.v_roue_gauche(param1)
                adapRS.v_roue_droite(param2)
                param1=None
                param2=None

                                                                                                                                                                                                                    
            else :
                if param1 =="carre":
                    strategy = faire_carre(strategy, environnement.vehicule)
                    controleur.executer_strategie(strategy)
                    param1 = None

                elif param1 == "mur":
                    strategy = proche_mur(strategy, environnement.vehicule)
                    controleur.executer_strategie(strategy)

                    
                    
            controleur3D.gerer_evenements()
            controleur2D.executer_strategie()

            environnement.bouger()
            environnement.temps.demarrer()
            environnement.rester_dans_limites()


        
            
        # Pause pour limiter la fréquence d'itération (environ 60 itérations/s)
        time.sleep(1/60)

        environnement.temps.arreter()