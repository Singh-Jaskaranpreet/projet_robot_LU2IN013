import sys
import threading

# Créez un événement global (ou à importer dans le main)
input_active = threading.Event()

class Controleur:
    def __init__(self,adaptateur):
        self.adaptateur = adaptateur
        self.choix = True

    def lire_commandes(self):
        """
        Lit les commandes de l'utilisateur.
        """
        global input_active
        while True:
            # Indique qu'on va saisir une commande
            input_active.set()
            try:
                if self.choix:
                    cmd = input("\nCommande (set_vRgd, set_vRg, set_vRd, get_distance, quitter) : ").strip()
                
            except EOFError:
                continue  # ou break selon votre besoin

            #Saisie terminée, on peut réactiver l'affichage de la simulation
            input_active.clear()
            if self.choix:
                # Traitement de la commande (exemple simple)
                if cmd.startswith("set_vRgd"):
                    try:
                        val = int(cmd.split()[1])
                        self.adaptateur.avancer(val)
                        print(f"[COMMANDE] accelerer de {val}")
                        #bug actuellement à corriger
                    except (IndexError, ValueError):
                        print("Utilisation : accelerer <valeur>")
                elif cmd.startswith("set_vRg"):
                    try:
                        val = int(cmd.split()[1])
                        self.adaptateur.v_roue_gauche(val)
                        print(f"[COMMANDE] Vitesse roue gauche définie à {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : set_vRg <valeur>")
                elif cmd.startswith("set_vRd"):
                    try:
                        val = int(cmd.split()[1])
                        self.adaptateur.v_roue_droite(val)
                        print(f"[COMMANDE] Vitesse roue droite définie à {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : set_vRd <valeur>")
                elif cmd.startswith("get_distance"):
                    try:
                        val = self.adaptateur.get_distance()
                        print(f"[COMMANDE] Distance : {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : set_vRg <valeur>")
                elif cmd == "quitter":
                    print("[COMMANDE] Arrêt de la simulation.")
                    sys.exit(0)
                else:
                    print("Commande inconnue.")

    def executer_strategie(self):
        """
        Exécute la stratégie de contrôle.
        """
        if self.adaptateur.sequence:  # Si une séquence est définie
            if self.adaptateur.vehicule.get_distance() < 5:  # Vérifier s'il y a une collision
                print("                                                            ", end = "\r")
                print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                self.adaptateur.sequence = None  # Arrêter la stratégie
                self.adaptateur.vehicule.vit_Rd = 0
                self.adaptateur.vehicule.vit_Rg = 0
            elif not self.adaptateur.sequence.stop(self.adaptateur):  # Si la séquence n'est pas terminée
                self.adaptateur.sequence.step(self.adaptateur)  # Passer à l'étape suivante
            else:  # Si la séquence est terminée
                self.adaptateur.sequence = None  # Réinitialiser la séquence