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
        vehicule.vit_Rg = 50
        vehicule.vit_Rd = 50
        self.parcouru += 1
    
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
        if self.angle_cible > 0:
            if self.angle_parcouru >= self.angle_cible:
                vehicule.vit_Rg = 0
                vehicule.vit_Rd = 0
                return True
            else:
                return False
        elif self.angle_cible < 0:
            if self.angle_parcouru <= self.angle_cible:
                vehicule.vit_Rg = 0
                vehicule.vit_Rd = 0
                return True
            else:
                return False
        else:
            return True

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
