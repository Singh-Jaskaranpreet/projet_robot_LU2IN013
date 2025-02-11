import pygame
from environnement import *

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1200, 800
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation de Véhicule")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

def afficher(screen, couleur_vehicule, couleur_texte, objects, environnement):
        """
        Affiche l'environnement, y compris le véhicule, les objets (obstacles),
        et la vitesse du véhicule.
        """

        screen.fill(BLANC) # Remplir l'écran en blanc

        # Afficher le véhicule sous forme de triangle
        points_triangle = environnement.position_des_roues(environnement.vehicule.p_centre)
        pygame.draw.polygon(screen, couleur_vehicule, points_triangle)

        # Dessiner la roue arrière
        pygame.draw.circle(screen, (0, 0, 0), (int(points_triangle[0][0]), int(points_triangle[0][1])), 3)

        # Dessiner les roues avant (ovales) avec la rotation du braquage
        largeur_roue = 10  # Largeur de l'ellipse
        hauteur_roue = 5  # Hauteur de l'ellipse
        
        for roue in [points_triangle[1],points_triangle[2]]:
            x, y = roue
            rect = pygame.Rect(x - largeur_roue // 2, y - hauteur_roue // 2, largeur_roue, hauteur_roue)

            # Appliquer l'orientation globale (vehicule.angle) + l'angle des roues (vehicule.angle_braquage)
            rotation_totale = environnement.vehicule.angle
            surface_roue = pygame.Surface((largeur_roue, hauteur_roue), pygame.SRCALPHA)
            pygame.draw.ellipse(surface_roue, (0, 0, 0), (0, 0, largeur_roue, hauteur_roue))

            # Appliquer la rotation
            surface_roue = pygame.transform.rotate(surface_roue, -rotation_totale)
            rect = surface_roue.get_rect(center=(x, y))
            screen.blit(surface_roue, rect.topleft)

        # Afficher les objets (obstacles)
        for obj in objects:
            pygame.draw.polygon(screen, (0, 0, 0), obj)


        # Afficher la vitesse du véhicule à l'écran
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {round(abs((environnement.vehicule.vit_Rd+environnement.vehicule.vit_Rg)/2), 3)} pixel/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))
        distance = font.render(f"Distance:{environnement.vehicule.mesurer_distance_obstacle(environnement)} pixel", True, couleur_texte)
        screen.blit(distance, (10, 40))
        vitesse = font.render(f"vitesse droite = {environnement.vehicule.vit_Rd}, vitesse gauche {environnement.vehicule.vit_Rg}", True, couleur_texte)
        screen.blit(vitesse, (10, 770))
        pygame.display.flip() # Met à jour l'écran

# Fonction pour afficher les instructions
def afficher_instructions():
    font = pygame.font.SysFont(None, 36)
    
    # Créer le texte des instructions
    instructions = [
        "Instructions :",
        "Flèche haut  : Accélérer et se deplacer suivant la direction",
        "Flèche bas  : Deccélérer et se deplacer suivant la direction",
        "Flèche droite  : Tourner a droite",
        "Flèche gauche  : Tourner a gauche",
        "Barre d'espace : Arrêter le véhicule",
        "Touche R : Réinitialiser la position",
        "Appuyez sur une touche pour commencer"
    ]
    
    screen.fill(BLANC)  # Remplir l'écran en blanc
    y_offset = 20 # Position de départ pour l'affichage des instructions
    
    for line in instructions:
        text = font.render(line, True, NOIR)
        screen.blit(text, (LARGEUR // 4, y_offset))  # Affiche chaque ligne de texte
        y_offset += 100  # Espacement entre les lignes
    
    pygame.display.flip()  # Met à jour l'écran
