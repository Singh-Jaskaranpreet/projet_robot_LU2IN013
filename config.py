from ursina import color  # Importer color depuis ursina

# Affichae 2D
# Dimensions de la fenêtre
LARGEUR = 1200
HAUTEUR = 800

# Couleurs (Blanc, Noir, Rouge, Vert)
COULEURS = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)]

# Paramètres pour les roues
LARGEUR_ROUE = 100  # Largeur de l'ellipse pour les roues
HAUTEUR_ROUE = 5   # Hauteur de l'ellipse pour les roues

# Autres paramètres
VITESSE_ECHELLE = 0.003


# Affichae 3D
# Couleurs utilisées
COULEURS = {'sol': color.white,'vehicule': color.red,'roue': color.black,'obstacle_rect': color.magenta,'obstacle_circulaire': color.blue}

# Paramètres du véhicule
ESSIEUX = 10  # Distance entre les roues avant et arrière
TAILLE_ROUE = 2  # Taille des roues (rayon de la sphère)

# Paramètres de la caméra
CAMERA_POSITION = (0, 50, -200)  # Position initiale de la caméra