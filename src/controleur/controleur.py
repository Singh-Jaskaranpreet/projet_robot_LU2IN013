import sys
import threading

# Créez un événement global (ou à importer dans le main)
input_active = threading.Event()

class Controleur:
    def __init__(self,adapVS,adapVF):
        self.adapVF = adapVF
        self.adapVS = adapVS
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
                    cmd = input("\nCommande (accelerer, freiner, reculer, set_vRg, set_vRd, acr_Rg, acr_Rd, get_distance, quitter) : ").strip()
                rep=input("Vouler vous faire un mouvement ou une strategie?")
                if rep == "mouvement":
                        v_rg=float(input("Donner une vitesse à la roue gauche(degree par seconde):"))
                        v_rd=float(input("Donner une vitesse à la roue droite(degree par seconde):"))
                        mouvement = (v_rg,v_rd)
                        self.adapVF.gerer_mouvements(mouvement)
                        self.adapVS.gerer_mouvements(mouvement)
                elif rep == "strategie":
                    strategie = input("Donner une stratégie:")
                    self.adapVF.gerer_mouvements(strategie)
                    self.adapVS.gerer_mouvements(strategie)
            except EOFError:
                continue  # ou break selon votre besoin

            #Saisie terminée, on peut réactiver l'affichage de la simulation
            input_active.clear()
            if self.choix:
                # Traitement de la commande (exemple simple)
                if cmd.startswith("accelerer"):
                    try:
                        val = int(cmd.split()[1])
                        self.adapVS.vehicule.set_vrg(self.adapVS.vehicule.vit_Rg + val)
                        self.adapVS.vehicule.set_vrd(self.adapVS.vehicule.vit_Rd + val)
                        print(f"[COMMANDE] accelerer de {val}")
                        #bug actuellement à corriger
                    except (IndexError, ValueError):
                        print("Utilisation : accelerer <valeur>")
                if cmd.startswith("freiner"):
                    try:
                        val = int(cmd.split()[1])
                        self.adapVS.vehicule.freiner(val)
                        print(f"[COMMANDE] freiner de {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : freiner <valeur>")
                if cmd.startswith("set_vRg"):
                    try:
                        val = int(cmd.split()[1])
                        self.adapVS.vehicule.set_vrg(val)
                        print(f"[COMMANDE] Vitesse roue gauche définie à {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : set_vRg <valeur>")
                if cmd.startswith("set_vRd"):
                    try:
                        val = int(cmd.split()[1])
                        self.adapVS.vehicule.set_vrd(val)
                        print(f"[COMMANDE] Vitesse roue droite définie à {val}")
                    except (IndexError, ValueError):
                        print("Utilisation : set_vRd <valeur>")
                if cmd == "quitter":
                    print("[COMMANDE] Arrêt de la simulation.")
                    sys.exit(0)
                else:
                    print("Commande inconnue.")

    def executer_strategie(self):
        if self.adapVS.sequence:  # Si une séquence est définie
            if self.adapVS.vehicule.environnement.collision():  # Vérifier s'il y a une collision
                print("                                                            ", end = "\r")
                print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                self.adapVS.sequence = None  # Arrêter la stratégie
                self.adapVS.vehicule.vit_Rd = 0
                self.adapVS.vehicule.vit_Rg = 0
            elif not self.adapVS.sequence.stop(self.adapVS):  # Si la séquence n'est pas terminée
                self.adapVS.sequence.step(self.adapVS)  # Passer à l'étape suivante
            else:  # Si la séquence est terminée
                self.adapVS.sequence = None  # Réinitialiser la séquence