import math as m
# Classe Véhicule
class Vehicule:

    def __init__(self, nom, p_centre,empattement,essieux,environnement, angle = 0):
        self.nom = nom
        self.long=empattement
        self.essieux = essieux
        self.angle = angle %360
        self.p_centre = p_centre
        self.vit_Rg = 0
        self.vit_Rd = 0
        self.starting_point_x=p_centre[0]
        self.starting_point_y=p_centre[1]
        self.nb_roues = 3
        self.environnement = environnement

    
    def accelerer(self, val):
        self.vit_Rg = min(150,self.vit_Rg+val)
        self.vit_Rd = min(150,self.vit_Rd+val)
    
    def freiner(self, val):
        if self.vit_Rg > 0:
            self.vit_Rg = max(0,self.vit_Rg-val)
        elif self.vit_Rg < 0:
            self.vit_Rg = min(0,self.vit_Rg+val)
        if self.vit_Rd > 0:
            self.vit_Rd = max(0,self.vit_Rd-val)
        elif self.vit_Rd < 0:
            self.vit_Rd = min(0,self.vit_Rd+val)

    def reculer(self, val):
        self.vit_Rg = max(-50, self.vit_Rg - val)
        self.vit_Rd = max(-50, self.vit_Rd - val)


    def restart(self):
        self.p_centre=[self.starting_point_x,self.starting_point_y]
        self.angle = 0
        self.vit_Rd=0
        self.vit_Rg=0
        

    def mesurer_distance_obstacle(self, environnement):
        """ Simule un capteur infrarouge détectant la distance jusqu'au premier obstacle en face du véhicule. """
    
        # 🔹 Position du capteur (au centre des roues avant)
        roues = environnement.position_des_roues(self.p_centre)
        capteur_x = (roues[1][0] + roues[2][0]) / 2
        capteur_y = (roues[1][1] + roues[2][1]) / 2

        # 🔹 Paramètres du capteur
        max_distance = 1000  # Distance maximale du capteur (en pixels)
        pas = 5  # Précision du scan (plus petit = plus précis)
        direction_angle = m.radians(self.angle)  # Convertir l'angle en radians

        # 🔹 Scanner point par point en ligne droite
        for d in range(0, max_distance, pas):
            point_x = capteur_x + d * m.cos(direction_angle)
            point_y = capteur_y + d * m.sin(direction_angle)

            # Vérifier si ce point touche un obstacle
            for obj in environnement.objects:
                # 🔴 Cas 1 : L'obstacle est un `pygame.Rect`
                if len(obj) == 4:
                    #print(f"obstacle rectangulaire de coordonée : {obj}", end = "\r")
                    if (obj[0][0] <= point_x <= obj[2][0]) and (obj[0][1] <= point_y <= obj[2][1]):
                        print(f" Détection d'un obstacle rectangle custom à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté
                # 🔵 Cas 2 : L'obstacle est un objet avec `x`, `y` et un `rayon` (cercle)
                elif len(obj) == 2:
                    #print(f"obstacle circulaire de coordonée : {obj}", end = "\r")
                    distance_objet = m.sqrt((point_x - obj[0][0]) ** 2 + (point_y - obj[0][1]) ** 2)
                    if distance_objet <= obj[1]:
                        print(f" Détection d'un obstacle circulaire à {d} px !", end = "\r")
                        return d  # Distance au premier obstacle détecté
        #print("                                                       ", end ="\r")
        #print(f" Aucun obstacle détecté, distance max : {max_distance}", end = "\r")
        return max_distance  # Aucune collision détectée