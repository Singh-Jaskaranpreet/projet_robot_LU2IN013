from ..adaptateurs import AdaptateurVF,AdaptateurVS



class Controleur:
    def __init__(self,adapVS,adapVF):
        self.adapVF = adapVF
        self.adapVS = adapVS

    def mouvements(self):
        rep=input("Vouler vous faire un mouvement ou une strategie?")
        if rep == "mouvement":
            v_rg=float(input("Donner une vitesse à la roue gauche:"))
            v_rd=float(input("Donner une vitesse à la roue droite:"))
            mouvement = (v_rg,v_rd)
            self.adapVF.gerer_mouvements(mouvement)
            self.adapVS.gerer_mouvements(mouvement)
        elif rep == "strategie":
            strategie = input("Donner une stratégie:")
            self.adapVF.gerer_mouvements(strategie)
            self.adapVS.gerer_mouvements(strategie)


    def executer_strategie(self):
        if self.adapVS.sequence:  # Si une séquence est définie
            if self.adapVS.vehicule.environnement.collision():  # Vérifier s'il y a une collision
                print("                                                            ", end = "\r")
                print("Collision détectée ! Arrêt de la stratégie.", end = "\r")
                self.adapVS.sequence = None  # Arrêter la stratégie
                self.adapVS.vehicule.vit_Rd = 0
                self.adapVS.vehicule.vit_Rg = 0
            elif not self.adapVS.sequence.stop(self.vehicule):  # Si la séquence n'est pas terminée
                self.adapVS.sequence.step(self.vehicule)  # Passer à l'étape suivante
            else:  # Si la séquence est terminée
                self.adapVS.sequence = None  # Réinitialiser la séquence
        
        
    

    