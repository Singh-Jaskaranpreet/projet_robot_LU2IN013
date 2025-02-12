import math as m

class Infrarouge():

    def __init__(self):
        pass

    def mesurer_distance_obstacle(self, environnement):
        """ Simule un capteur infrarouge détectant la distance jusqu'au premier obstacle en face du véhicule. """
    
        # 🔹 Position du capteur (au centre des roues avant)
        roues = environnement.vehicule.position_des_roues(environnement.vehicule.p_centre)
        capteur_x = (roues[1][0] + roues[2][0]) / 2
        capteur_y = (roues[1][1] + roues[2][1]) / 2

        # 🔹 Paramètres du capteur
        max_distance = 1000  # Distance maximale du capteur (en pixels)
        pas = 5  # Précision du scan (plus petit = plus précis)
        direction_angle = m.radians(environnement.vehicule.angle)  # Convertir l'angle en radians

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
                        return d  # Distance au premier obstacle détecté
                # 🔵 Cas 2 : L'obstacle est un objet avec `x`, `y` et un `rayon` (cercle)
                elif len(obj) == 2:
                    #print(f"obstacle circulaire de coordonée : {obj}", end = "\r")
                    distance_objet = m.sqrt((point_x - obj[0][0]) ** 2 + (point_y - obj[0][1]) ** 2)
                    if distance_objet <= obj[1]:
                        return d  # Distance au premier obstacle détecté
        return max_distance  # Aucune collision détectée