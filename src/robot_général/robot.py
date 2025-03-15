class Robot:
    def __init__(self, vehicule, type_adaptateur):
        # Choisir l'adaptateur en fonction du type
        if type_adaptateur == 'RS':
            self.adaptateur = AdaptateurRS(vehicule)
        else:
            self.adaptateur = AdaptateurRR(vehicule)

    def avancer(self, valeur):
        self.adaptateur.avancer(valeur)

    def arreter(self):
        self.adaptateur.arreter()

    def v_roue_gauche(self, valeur):
        self.adaptateur.v_roue_gauche(valeur)

    def v_roue_droite(self, valeur):
        self.adaptateur.v_roue_droite(valeur)

    def distance_parcouru(self, vit, temps):
        return self.adaptateur.distance_parcouru(vit, temps)

    def get_distance(self):
        return self.adaptateur.get_distance()

    def get_temps(self, vitesse):
        return self.adaptateur.get_temps(vitesse)

    def get_essieux(self):
        return self.adaptateur.get_essieux()

    def get_vitesse_Rg(self):
        return self.adaptateur.get_vitesse_Rg()

    def get_vitesse_Rd(self):
        return self.adaptateur.get_vitesse_Rd()
