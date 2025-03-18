import math as m

class StrategyAsync:
    def start(self, vehicule):
        pass
    
    def step(self, vehicule):
        pass
    
    def stop(self, vehicule):
        return True

class AvancerDroitStrategy(StrategyAsync):
    def __init__(self, distance):
        self.distance = distance
        self.parcouru = 0
        self.vitesse = 50
        
    def start(self, vehicule):
        self.parcouru = 0

    def step(self, vehicule):
        vehicule.reset()
        vehicule.avancer(self.vitesse)
        
        # Calculer le temps écoulé depuis la dernière itération
        current_time = vehicule.get_temps()
       
        # Mettre à jour la distance parcourue
        self.parcouru += vehicule.distance_parcouru(self.vitesse)
        #print(self.parcouru)

    def stop(self, vehicule):
        if vehicule.get_distance() < 20:
            vehicule.arreter()
            return True
        if self.parcouru >= self.distance:
            vehicule.arreter()
            return True
        return False

class TournerAngleStrategy(StrategyAsync):
    def __init__(self, angle):
        # angle cible en degrés (positif pour gauche, négatif pour droite)
        self.angle_cible = angle  
        self.angle_parcouru = 0  
        self.vitesse_rotation = 30  # vitesse utilisée pour la roue active durant le virage

    def start(self, vehicule):
        self.angle_parcouru = 0
        

    def step(self, vehicule):
        vehicule.reset()
        if self.angle_cible > 0:
            # Virage à gauche
            vehicule.v_roue_gauche(0)
            vehicule.v_roue_droite(self.vitesse_rotation)
            omega = self.vitesse_rotation /  vehicule.get_essieux()
        else:
            # Virage à droite
            vehicule.v_roue_gauche(self.vitesse_rotation)
            vehicule.v_roue_droite(0)
            omega = self.vitesse_rotation /  vehicule.get_essieux()

        dt = vehicule.get_temps()

        # On prend la valeur absolue pour éviter les erreurs de direction
        angle_cible_abs = abs(self.angle_cible)

        # Calcul de l'incrément d'angle en degrés
        dtheta = m.degrees(omega * dt)
        self.angle_parcouru += abs(dtheta)  # On accumule en valeur absolue

    def stop(self, vehicule):
        # Arrêter le virage lorsque l'angle accumulé atteint l'angle cible
        if self.angle_parcouru >= abs(self.angle_cible) -1 or vehicule.get_distance() < 20:
            vehicule.arreter()
            return True
        return False
    
class StrategieSequence(StrategyAsync):
    def __init__(self, strategies):
        self.strategies = strategies
        self.index = 0
    
    def start(self, vehicule):
        if self.strategies:
            self.strategies[0].start(vehicule)
    
    def step(self, vehicule):
        if self.index < len(self.strategies):
            strategie = self.strategies[self.index]
            if not strategie.stop(vehicule):
                strategie.step(vehicule)
            else:
                self.index += 1
                if self.index < len(self.strategies):
                    self.strategies[self.index].start(vehicule)
    
    def stop(self, vehicule):
        return self.index >= len(self.strategies)
    
class AccelererStrategy(StrategyAsync):
    def __init__(self):
        self.distance_obstacle = 0
        self.vitesse_max = 1000
        self.vitesse_depart = 10

    def start(self, vehicule):
        self.distance_obstacle = vehicule.get_distance()

    def step(self, vehicule):
        if 0 < vehicule.get_vitesse_Rg() < self.vitesse_max:
            vehicule.avancer(vehicule.get_vitesse_Rg()+50)
        elif vehicule.get_vitesse_Rg() == 0:
            vehicule.avancer(self.vitesse_depart)
        self.distance_obstacle = vehicule.get_distance()

    def stop(self,vehicule):
        if self.distance_obstacle < 100:
            vehicule.arreter()
            return True
        return False
    
class DoucementStrategy(StrategyAsync):
    def __init__(self):
        self.vitesse_min = 20

    def start(self, vehicule):
        self.distance_obstacle = vehicule.get_distance()
    
    def step(self, vehicule):
        
        vehicule.avancer(self.vitesse_min)

        self.distance_obstacle = vehicule.get_distance()

    def stop(self, vehicule):
        if self.distance_obstacle < 20  :
            vehicule.arreter()
            return True
        return False

#la startegy pour suivre un objet n'est pas encore fonctionelle une mise à jour est nécessaire
class SuivreObjetStrategy(StrategyAsync):
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
        if vehicule.get_distance() < obstacle_d:
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