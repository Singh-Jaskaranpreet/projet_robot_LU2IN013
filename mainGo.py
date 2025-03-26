from src.controleur import Controleur
from src.controleur.strategy import *
from Robot2IN013 import Robot2IN013

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
while True:

    robot = Robot2IN013()
    adapRR = AdaptateurRR(robot)
    controleur = Controleur(adapRR)

    if param2 is not None:
            adapRR.set_VrG(param1)
            adapRR.set_VrD(param2)
            param1=None
            param2=None

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
