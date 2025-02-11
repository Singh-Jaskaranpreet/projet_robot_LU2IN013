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
        self.angle_cible = angle
        self.angle_parcouru = 0
    
    def start(self, vehicule):
        self.angle_parcouru = 0

    def step(self, vehicule):
        vitesse_rotation = 10
        vehicule.vit_Rg = -vitesse_rotation
        vehicule.vit_Rd = vitesse_rotation

        self.angle_parcouru += m.degrees((vehicule.vit_Rd - vehicule.vit_Rg) / vehicule.essieux * vehicule.temps.get_temps_ecoule())
        
        # Simulation d'un pas de rotation
        
    def stop(self, vehicule):
        if self.angle_parcouru >= self.angle_cible:
            vehicule.vit_Rg = 0
            vehicule.vit_Rd = 0
        return abs(self.angle_parcouru) >=self.angle_cible

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
