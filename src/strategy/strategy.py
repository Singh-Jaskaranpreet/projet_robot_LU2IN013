import math as m
import time
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
        self.start_time = time.time()
        self.last_time = self.start_time  # Initialiser le temps de la dernière itération

    def step(self, vehicule):
        vehicule.set_vrd(50)
        vehicule.set_vrg(50)
        
        # Calculer le temps écoulé depuis la dernière itération
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        self.last_time = current_time  # Mettre à jour le temps de la dernière itération
        
        # Mettre à jour la distance parcourue
        self.parcouru += round(0.003*(abs((abs(vehicule.vit_Rd)+abs(vehicule.vit_Rg))/2)),3) * elapsed_time

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
        self.start_time = time.time()
        self.last_time = self.start_time

    def step(self, vehicule):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        if self.angle_cible > 0:
            # Virage à gauche : faire pivoter autour de la roue gauche (pivot = vit_Rg)
            vehicule.vit_Rg = 0
            vehicule.vit_Rd = self.vitesse_rotation
            # La vitesse angulaire est donnée par omega = vitesse_active / empattement (en rad/s)
            omega = self.vitesse_rotation / vehicule.essieux
            # Calcul de l'incrément d'angle en degrés
            dtheta = m.degrees(omega * dt)
            self.angle_parcouru += dtheta
            
        elif self.angle_cible < 0:
            # Virage à droite : faire pivoter autour de la roue droite (pivot = vit_Rd)
            vehicule.vit_Rd = 0
            vehicule.vit_Rg = self.vitesse_rotation
            # Dans ce cas, omega sera négatif
            omega = -self.vitesse_rotation / vehicule.essieux
            dtheta = m.degrees(omega * dt)
            self.angle_parcouru += dtheta

    def stop(self, vehicule):
        # Arrêter le virage lorsque l'angle accumulé atteint (ou dépasse) l'angle cible.

        if abs(self.angle_parcouru) >= self.angle_cible -0.1:
            vehicule.vit_Rg = 0
            vehicule.vit_Rd = 0
            return True
        else:
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


