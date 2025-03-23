from ursina import color  # Importer color depuis ursina

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


# Affichage 3D
# Couleurs utilisées
COULEURS_3D = {'sol': color.white,'vehicule': color.red,'roue': color.black,'obstacle_rect': color.magenta,'obstacle_circulaire': color.blue}

# Paramètres du véhicule
ESSIEUX = 10  # Distance entre les roues avant et arrière
TAILLE_ROUE = 2  # Taille des roues (rayon de la sphère)

# Paramètres de la caméra
CAMERA_POSITION = (0, 50, -200)  # Position initiale de la caméra