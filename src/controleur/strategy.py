import math as m
import config

class StrategyAsync:
    def start(self, vehicule):
        pass
    
    def step(self, vehicule): 
        pass
    
    def stop(self, vehicule):
        return True

class AvancerDroitStrategy(StrategyAsync):
    """
    Stratégie pour avancer droit sur une distance donnée.
    """
    def __init__(self, distance):
        self.distance = distance
        self.parcouru = config.PARCOURUE
        self.vitesse = config.VITESSE
        
    def start(self, vehicule):
        self.parcouru = 0

    def step(self, vehicule):
        vehicule.reset()
        vehicule.avancer(self.vitesse)
       
        # Mettre à jour la distance parcourue
        self.parcouru += vehicule.get_distance_parcouru(self.vitesse)
        #print(self.parcouru)
        print(f'j ai parcourue au totale {self.parcouru}')

    def stop(self, vehicule):
        print(f'la distance ciblé est de {self.distance}')
        if vehicule.get_distance_to_obstacle() < config.echelle(20):
            print("Obstacle détecté, arrêt de la stratégie.")
            vehicule.arreter()
            return True
        print(f'la condition d arrete vaut {self.parcouru >= self.distance}')
        if self.parcouru >= self.distance:
            print("Distance cible atteinte, arrêt de la stratégie.")
            vehicule.arreter()
            return True
        return False

class TournerAngleStrategy(StrategyAsync):
    """
    Stratégie pour tourner d'un angle donné.
    """
    def __init__(self, angle):
        # angle cible en degrés (positif pour gauche, négatif pour droite)
        self.angle_cible = angle  
        self.angle_parcouru = config.ANGLE_PARCOURU 
        self.vitesse_rotation = config.VITESSE_ROTATION  # vitesse utilisée pour la roue active durant le virage

    def start(self, vehicule):
        self.angle_parcouru = 0
        

    def step(self, vehicule):
        vehicule.reset()
        if self.angle_cible > 0:
            # Virage à gauche
            vehicule.set_VrG(0)
            vehicule.set_VrD(self.vitesse_rotation)
        else:
            # Virage à droite
            vehicule.set_VrG(self.vitesse_rotation)
            vehicule.set_VrD(0)


        # Calcul de l'incrément d'angle en degrés
        dtheta = m.degrees(vehicule.get_angle_parcourueRad(self.vitesse_rotation))
        self.angle_parcouru += abs(dtheta)  # On accumule en valeur absolue

    def stop(self, vehicule):
        print(f'on a parcourue {self.angle_parcouru}')
        # Arrêter le virage lorsque l'angle accumulé atteint l'angle cible
        if self.angle_parcouru >= abs(self.angle_cible) -1 or vehicule.get_distance_to_obstacle() < config.echelle(20):
            vehicule.arreter()
            return True
        return False
    
class StrategieSequence(StrategyAsync):
    """
    Stratégie pour exécuter une séquence de stratégies.
    """
    def __init__(self, strategies):
        self.strategies = strategies
        self.index = 0
    
    def start(self, vehicule):
        if self.strategies:
            self.strategies[0].start(vehicule)
    
    def step(self, vehicule):
        if self.index < len(self.strategies):
            print(f"Exécution de la stratégie {self.index + 1}/{len(self.strategies)}")
            strategie = self.strategies[self.index]
            if not strategie.stop(vehicule):
                strategie.step(vehicule)
            else:
                print(f"Stratégie {self.index + 1} terminée.")
                self.index += 1
                if self.index < len(self.strategies):
                    self.strategies[self.index].start(vehicule)

    def stop(self, vehicule):
        return self.index >= len(self.strategies)
    
class AccelererStrategy(StrategyAsync):
    """
    Stratégie pour accélérer jusqu'à être à une distance (100) d'un obstacle.
    """
    def __init__(self):
        self.distance_obstacle = config.DISTANCE_OBSTACLE
        self.vitesse_max = config.VITESSE_MAX
        self.vitesse_depart = config.VITESSE_DEPART

    def start(self, vehicule):
        self.distance_obstacle = vehicule.get_distance_to_obstacle()

    def step(self, vehicule):
        if 0 < vehicule.get_VrG() < self.vitesse_max:
            vehicule.avancer(vehicule.get_VrG()+20)
        elif vehicule.get_VrG() == 0:
            vehicule.avancer(self.vitesse_depart)
        self.distance_obstacle = vehicule.get_distance_to_obstacle()

    def stop(self,vehicule):
        if self.distance_obstacle < config.echelle(50):
            return True
        return False
    
class DoucementStrategy(StrategyAsync):
    """
    Stratégie pour avancer doucement jusqu'à être proche d'un obstacle.
    """
    def __init__(self):
        self.vitesse_min = config.VITESSE_MIN

    def start(self, vehicule):
        self.distance_obstacle = vehicule.get_distance_to_obstacle()
    
    def step(self, vehicule):
        if vehicule.get_VrG() > self.vitesse_min:
            vehicule.avancer(vehicule.get_VrG()-20)
        self.distance_obstacle = vehicule.get_distance_to_obstacle()

    def stop(self, vehicule):
        if self.distance_obstacle < config.echelle(20)  :
            vehicule.arreter()
            return True
        return False

#la startegy pour suivre un objet n'est pas encore fonctionelle une mise à jour est nécessaire
class SuivreObjetStrategy(StrategyAsync):
    """
    Stratégie pour suivre un objet en mouvement.
    """
    def __init__(self):
        print("la startegy pour suivre un objet n'est pas encore fonctionnelle merci de pateinter jusqu'à la prochaine mise à jour")
        return
        self.target = None
        self.current_strategy = None  # Stratégie en cours (tourner ou avancer)

    def start(self, vehicule):
        return
        # On ne stocke plus une position statique, mais on mettra à jour dynamiquement
        if vehicule.environnement.asuivre:
            self.target = vehicule.environnement.asuivre  # Référence directe à la liste
        else:
            self.target = None
        self.current_strategy = None

    def step(self, vehicule):
        return

        dt = vehicule.environnement.temps.get_temps_ecoule()

        # Vérification si un obstacle est proche
        obstacle_d = 50  # Distance seuil en pixels
        if vehicule.get_distance_to_obstacle() < obstacle_d:
            # Activer une stratégie d'évitement
            avoidance_angle = 30  # Tourner de 30° pour éviter l'obstacle
            if self.current_strategy is None or not isinstance(self.current_strategy, TournerAngleStrategy):
                self.current_strategy = TournerAngleStrategy(avoidance_angle)
                self.current_strategy.start(vehicule)
            else:
                self.current_strategy.step(vehicule)
                if self.current_strategy.stop(vehicule):
                    self.current_strategy = None
            return  # Sortir du step() pour cette itération

        # Mise à jour dynamique de la position de la cible
        if not self.target or not self.target[0]:
            return  # Si la cible n'existe pas ou a été supprimée

        # Prendre la position actuelle de la cible
        tx, ty = self.target[0]  

        # Calcul de l'angle entre le véhicule et la cible
        vx, vy = vehicule.p_centre
        angle_target = m.degrees(m.atan2(ty - vy, tx - vx))
        angle_diff = (angle_target - vehicule.angle + 180) % 360 - 180

        # Vérifier si l'angle est aligné avec la cible
        if abs(angle_diff) > 5:
            if self.current_strategy is None or not isinstance(self.current_strategy, TournerAngleStrategy):
                self.current_strategy = TournerAngleStrategy(angle_diff)
                self.current_strategy.start(vehicule)
            else:
                self.current_strategy.step(vehicule)
                if self.current_strategy.stop(vehicule):
                    self.current_strategy = None
        else:
            # Une fois aligné, avancer vers la cible
            distance = m.sqrt((tx - vx)**2 + (ty - vy)**2)
            if self.current_strategy is None or not isinstance(self.current_strategy, AvancerDroitStrategy):
                self.current_strategy = AvancerDroitStrategy(distance)
                self.current_strategy.start(vehicule)
            else:
                self.current_strategy.step(vehicule)
                if self.current_strategy.stop(vehicule):
                    self.current_strategy = None

    def stop(self, vehicule):
        return True
        # Arrêter la stratégie si la cible est atteinte
        if not self.target or not self.target[0]:
            return True
        vx, vy = vehicule.get_centre()
        tx, ty = self.target[0]
        distance = m.sqrt((tx - vx)**2 + (ty - vy)**2)
        if distance < 20: # Seuil ajustable
            vehicule.vit_Rg = 0
            vehicule.vit_Rd= 0
            vehicule.environnement.asuivre_act = False
            return True  
        return distance < 20
    
def faire_carre(strategy, vehicule):
    """
    Fait faire un carré au robot
    :return None
    """
    strategy = StrategieSequence([AvancerDroitStrategy(0.75), TournerAngleStrategy(90)] * 4)
    strategy.start(vehicule)
    return strategy

def proche_mur(startegy, vehicule):
    """
    Se rapproche le plus possible d'un mur devant lui
    :return: None
    """
    strategy = StrategieSequence([AccelererStrategy(), DoucementStrategy()])
    strategy.start(vehicule)
    return strategy

    