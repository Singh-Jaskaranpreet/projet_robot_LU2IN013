import sys
import threading

# Créez un événement global (ou à importer dans le main)
input_active = threading.Event()

def lire_commandes(environnement):
    """
    Lit les commandes de l'utilisateur.
    """
    global input_active
    while True:
        # Indique qu'on va saisir une commande
        input_active.set()
        try:
            cmd = input("\nCommande (accelerer, freiner, reculer, set_vRg, set_vRd, acr_Rg, acr_Rd, get_distance, quitter) : ").strip()
        except EOFError:
            continue  # ou break selon votre besoin

        # Saisie terminée, on peut réactiver l'affichage de la simulation
        input_active.clear()

        # Traitement de la commande (exemple simple)
        if cmd.startswith("accelerer"):
            try:
                val = int(cmd.split()[1])
                environnement.vehicule.set_vrg(environnement.vehicule.vit_Rg + val)
                environnement.vehicule.set_vrd(environnement.vehicule.vit_Rd + val)
                print(f"[COMMANDE] accelerer de {val}")
                #bug actuellement à corriger
            except (IndexError, ValueError):
                print("Utilisation : accelerer <valeur>")
        if cmd.startswith("freiner"):
            try:
                val = int(cmd.split()[1])
                environnement.vehicule.freiner(val)
                print(f"[COMMANDE] freiner de {val}")
            except (IndexError, ValueError):
                print("Utilisation : freiner <valeur>")
        if cmd.startswith("set_vRg"):
            try:
                val = int(cmd.split()[1])
                environnement.vehicule.set_vrg(val)
                print(f"[COMMANDE] Vitesse roue gauche définie à {val}")
            except (IndexError, ValueError):
                print("Utilisation : set_vRg <valeur>")
        if cmd.startswith("set_vRd"):
            try:
                val = int(cmd.split()[1])
                environnement.vehicule.set_vrd(val)
                print(f"[COMMANDE] Vitesse roue droite définie à {val}")
            except (IndexError, ValueError):
                print("Utilisation : set_vRd <valeur>")
        if cmd == "quitter":
            print("[COMMANDE] Arrêt de la simulation.")
            sys.exit(0)
        else:
            print("Commande inconnue.")

def info(environnement) :
    print(
        f"\nPosition: {environnement.vehicule.p_centre}, "
        f"Vitesse G: {environnement.vehicule.vit_Rg}, "
        f"Vitesse D: {environnement.vehicule.vit_Rd}, "
        f"Angle: {environnement.vehicule.angle}, "
        f"Distance obstacle: {environnement.vehicule.get_distance()}",
        end="\r"
    )