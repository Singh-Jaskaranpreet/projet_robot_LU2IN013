from ursina import color  # Importer color depuis ursina
import math


#-------------------------------------------------------------------------------------------------------#

# Affichage 2D
# Dimensions de la fenêtre
LARGEUR = 1200
HAUTEUR = 800

# Couleurs (Blanc, Noir, Rouge, Vert)
COULEURS_2D = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)]

# Paramètres pour les roues
LARGEUR_ROUE = 10  # Largeur de l'ellipse pour les roues
HAUTEUR_ROUE = 5   # Hauteur de l'ellipse pour les roues

# Autres paramètres
VITESSE_ECHELLE = 0.003

#Fonctions pour mettre l'echelle
def echelle(x):
    return round(VITESSE_ECHELLE * x, 3)

#-------------------------------------------------------------------------------------------------------#

# Affichage 3D
# Couleurs utilisées
COULEURS_3D = {'sol': color.white,'vehicule': color.red,'roue': color.black,'obstacle_rect': color.magenta,'obstacle_circulaire': color.blue}

# Paramètres du véhicule
ESSIEUX = 40  # Distance entre les roues avant et arrière
TAILLE_ROUE = 2  # Taille des roues (rayon de la sphère)

# Paramètres de la caméra
CAMERA_POSITION = (0, 50, -200)  # Position initiale de la caméra

#-------------------------------------------------------------------------------------------------------#

# Stratégie
#AvancerDroitStrategy(StrategyAsync)
PARCOURUE = 0
VITESSE = 50

#TournerAngleStrategy(StrategyAsync)
ANGLE_PARCOURU = 0
VITESSE_ROTATION = 30

#AccelererStrategy
DISTANCE_OBSTACLE = 0
VITESSE_MAX = 300
VITESSE_DEPART = 10

#class DoucementStrategy(StrategyAsync)
VITESSE_MIN = 10

#-------------------------------------------------------------------------------------------------------#

#AdaptateurRR
VITESSE_RG = 0
VITESSE_RD = 0
SEQUENCE = None


#-------------------------------------------------------------------------------------------------------#

#ROBOT SIMULE
VITESSE_RG = 0
VITESSE_RD = 0
NB_ROUES = 3
ANGLE_SERVO = 0