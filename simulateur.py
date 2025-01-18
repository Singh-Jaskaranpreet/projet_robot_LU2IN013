import pygame
import sys
from Vehicule import *
from Environnement import *

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1080, 800
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation de Véhicule")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Création de l'environnement et d'un véhicule
environnement = Environnement(LARGEUR, HAUTEUR)
vehicule = Vehicule("Voiture", 200, HAUTEUR // 2, 0, 4)

# Fonction pour afficher les instructions
def afficher_instructions():
    font = pygame.font.SysFont(None, 36)
    
    # Créer le texte des instructions
    instructions = [
        "Instructions :",
        "Flèche droite  : Accélérer et deplace vers la droite",
        "Flèche haut  : Accélérer et deplace vers le haut",
        "Flèche gauche et bas : Décélérer",
        "Barre d'espace : Arrêter le véhicule",
        "Touche R : Réinitialiser la position",
        "Appuyez sur une touche pour commencer"
    ]
    
    screen.fill(BLANC)  # Remplir l'écran en blanc
    y_offset = 10 # Position de départ pour l'affichage des instructions
    
    for line in instructions:
        text = font.render(line, True, NOIR)
        screen.blit(text, (LARGEUR // 4, y_offset))  # Affiche chaque ligne de texte
        y_offset += 100  # Espacement entre les lignes
    
    pygame.display.flip()  # Met à jour l'écran

# Afficher l'écran d'instructions avant de commencer
afficher_instructions()

# Attendre que l'utilisateur appuie sur une touche pour commencer
attente = True
while attente:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  # Une touche a été pressée
            attente = False  # On sort de la boucle et commence la simulation

# Boucle principale de la simulation
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()
    dir = vehicule.gerer_controles(keys)


    # Mise à jour des éléments
    if dir == 1:
        vehicule.bouger_x()
    elif dir == 2:
        vehicule.bouger_y()
    elif dir == 0 :
        vehicule.deceleration(0.5)
        dir=-1
    environnement.mise_a_jour(vehicule)

    # Affichage
    screen.fill(BLANC)
    environnement.afficher(screen, vehicule, ROUGE, NOIR)
    pygame.display.flip()
    clock.tick(60)
