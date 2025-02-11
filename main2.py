#!/usr/bin/env python3
import sys
import time
import threading
from environnement import Environnement
import controleur
import lcm  # Module contenant lire_commandes et input_active

# Initialiser last_print avant la boucle
last_print = time.time()

# Création de l'environnement et du véhicule
environnement = Environnement()
controleur_instance = controleur.Controleur(environnement.vehicule, environnement)

# Démarrer l'horloge du véhicule une seule fois
environnement.vehicule.temps.demarrer()

# Lancer la lecture des commandes dans un thread séparé
threading.Thread(target=lcm.lire_commandes, args=(environnement,), daemon=True).start()

# Boucle principale de la simulation (sans affichage graphique)
try:
    while True:
        # Exécuter la stratégie en cours (si applicable)
        controleur_instance.executer_strategie()

        # Mettre à jour la simulation
        environnement.bouger()
        environnement.rester_dans_limites()

        # Affichage des infos de simulation toutes les 1 seconde
        # seulement si l'utilisateur n'est pas en train de taper une commande
        if  time.time() - last_print > 2:
            last_print = time.time()
            print(
                f"\nPosition: {environnement.vehicule.p_centre}, "
                f"Vitesse G: {environnement.vehicule.vit_Rg}, "
                f"Vitesse D: {environnement.vehicule.vit_Rd}, "
                f"Angle: {environnement.vehicule.angle}, "
                f"Distance obstacle: {environnement.vehicule.get_distance(environnement)}",
                end="\r"
            )
        # Pause pour limiter la fréquence d'itération (environ 60 itérations/s)
        time.sleep(1/60)

except KeyboardInterrupt:
    print("\nSimulation arrêtée par l'utilisateur.")

finally:
    temps_total = environnement.vehicule.temps.arreter()
    print(f"\nTemps total de simulation: {temps_total} secondes")
    sys.exit(0)