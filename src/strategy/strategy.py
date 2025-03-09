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
    
    def start(self, vehicule):
        self.parcouru = 0
        

    def step(self, vehicule):
        vehicule.set_vrd(50)
        vehicule.set_vrg(50)
        
        # Calculer le temps écoulé depuis la dernière itération
        current_time = vehicule.environnement.temps.get_temps_ecoule()
       
        
        
        # Mettre à jour la distance parcourue
        self.parcouru += abs(round(0.003*(abs((abs(vehicule.vit_Rd)+abs(vehicule.vit_Rg))/2)),3) * current_time)
        #print(self.parcouru)

    def stop(self, vehicule):
        return self.parcouru >= self.distance

class TournerAngleStrategy(StrategyAsync):
    def __init__(self, angle):
        # angle cible en degrés (positif pour gauche, négatif pour droite)
        self.angle_cible = angle  
        self.angle_parcouru = 0  
        self.vitesse_rotation = 30  # vitesse utilisée pour la roue active durant le virage

    def start(self, vehicule):
        self.angle_parcouru = 0
        

    def step(self, vehicule):
        dt = vehicule.environnement.temps.get_temps_ecoule()

        # On prend la valeur absolue pour éviter les erreurs de direction
        angle_cible_abs = abs(self.angle_cible)

        if self.angle_cible > 0:
            # Virage à gauche
            vehicule.vit_Rg = 0
            vehicule.vit_Rd = self.vitesse_rotation
            omega = self.vitesse_rotation / vehicule.essieux
        else:
            # Virage à droite
            vehicule.vit_Rd = 0
            vehicule.vit_Rg = self.vitesse_rotation
            omega = -self.vitesse_rotation / vehicule.essieux

        # Calcul de l'incrément d'angle en degrés
        dtheta = m.degrees(omega * dt)
        self.angle_parcouru += abs(dtheta)  # On accumule en valeur absolue

    def stop(self, vehicule):
        # Arrêter le virage lorsque l'angle accumulé atteint l'angle cible
        if self.angle_parcouru >= abs(self.angle_cible) -1:
            vehicule.vit_Rg = 0
            vehicule.vit_Rd = 0
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

    def start(self, vehicule):
        self.distance_obstacle = vehicule.infrarouge.mesurer_distance_obstacle(vehicule)
    
    def step(self, vehicule):
        if vehicule.vit_Rg != vehicule.vit_Rd :
            if vehicule.vit_Rg > vehicule.vit_Rd :
                vehicule.vit_Rd = vehicule.vit_Rg
            else :
                vehicule.vit_Rg = vehicule.vit_Rd

        vehicule.accelerer(30)

        self.distance_obstacle = vehicule.infrarouge.mesurer_distance_obstacle(vehicule)

    def stop(self,vehicule):
        return self.distance_obstacle < 50
    
class DoucementStrategy(StrategyAsync):
    def __init__(self, vehicule):
        self.vitesse = 20
        self.angle = vehicule.angle % 90

    def start(self, vehicule):
        self.distance_obstacle = vehicule.infrarouge.mesurer_distance_obstacle(vehicule)
        if self.angle != 45 :
            self.angle = self.angle % 45
    
    def step(self, vehicule):
        
        if vehicule.vit_Rg > 29 :
            vehicule.freiner(20)

        self.distance_obstacle = vehicule.infrarouge.mesurer_distance_obstacle(vehicule)

    def stop(self, vehicule):
        if self.distance_obstacle < 20 + self.angle // 2  :
            vehicule.vit_Rg = 0
            vehicule.vit_Rd= 0
            return True
        return False


class SuivreObjetStrategy(StrategyAsync):
    def __init__(self):
        self.target = None
        self.current_strategy = None  # Stratégie en cours (tourner ou avancer)

    def start(self, vehicule):
        # On ne stocke plus une position statique, mais on mettra à jour dynamiquement
        if vehicule.environnement.asuivre:
            self.target = vehicule.environnement.asuivre  # Référence directe à la liste
        else:
            self.target = None
        self.current_strategy = None

    def step(self, vehicule):
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
        # Arrêter la stratégie si la cible est atteinte
        if not self.target or not self.target[0]:
            return True
        vx, vy = vehicule.p_centre
        tx, ty = self.target[0]
        distance = m.sqrt((tx - vx)**2 + (ty - vy)**2)
        if distance < 20: # Seuil ajustable
            vehicule.vit_Rg = 0
            vehicule.vit_Rd= 0
            vehicule.environnement.asuivre_act = False
            return True  
        return distance < 20