import pygame
import sys
from Vehicule import *
from Environnement import *
from random import *

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1200, 800
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation de Véhicule")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

# Création de l'environnement et d'un véhicule
environnement = Environnement(LARGEUR, HAUTEUR)
vehicule = Vehicule("Robot",0 , (200, HAUTEUR // 2), 75, nb_roues=3)


tmp=[pygame.Rect(randint(400, 900), randint(0,HAUTEUR//2), randint(10,100), randint(200,HAUTEUR//2))]


def afficher(screen, vehicule, couleur_vehicule, couleur_texte, objects):
        """
        Affiche l'environnement, y compris le véhicule, les objets (obstacles),
        et la vitesse du véhicule.
        """
        # Afficher le véhicule sous forme de triangle
        points_triangle = [vehicule.r_Ar, vehicule.r_Avg, vehicule.r_Avd]
        pygame.draw.polygon(screen, couleur_vehicule, points_triangle)

        # Dessiner les roues arrière
        pygame.draw.circle(screen, (0, 0, 0), (int(vehicule.r_Ar[0]), int(vehicule.r_Ar[1])), 3)

        # Dessiner les roues avant (ovales) avec la rotation du braquage
        largeur_roue = 10  # Largeur de l'ellipse
        hauteur_roue = 5  # Hauteur de l'ellipse

        for roue in [vehicule.r_Avg, vehicule.r_Avd]:
            x, y = roue
            rect = pygame.Rect(x - largeur_roue // 2, y - hauteur_roue // 2, largeur_roue, hauteur_roue)

            # Appliquer l'orientation globale (vehicule.angle) + l'angle des roues (vehicule.angle_braquage)
            rotation_totale = vehicule.angle + vehicule.angle_braquage
            surface_roue = pygame.Surface((largeur_roue, hauteur_roue), pygame.SRCALPHA)
            pygame.draw.ellipse(surface_roue, (0, 0, 0), (0, 0, largeur_roue, hauteur_roue))

            # Appliquer la rotation
            surface_roue = pygame.transform.rotate(surface_roue, -rotation_totale)
            rect = surface_roue.get_rect(center=(x, y))
            screen.blit(surface_roue, rect.topleft)

        # Afficher les objets (obstacles)
        for obj in objects:
            pygame.draw.rect(screen, (0, 0, 0), obj)


        # Afficher la vitesse du véhicule à l'écran
        font = pygame.font.SysFont(None, 36)
        vitesse_text = font.render(f"Vitesse: {round(abs(vehicule.vitesse * 2), 3)} m/s", True, couleur_texte)
        screen.blit(vitesse_text, (10, 10))


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


def in_limite(vehicule):
    for point in [vehicule.r_Ar, vehicule.r_Avg, vehicule.r_Avd]:
        if point[0] < 0 or point[0] > LARGEUR  or point[1] < 0 or point[1] > HAUTEUR :
            return False
    return True


def rester_dans_limites(vehicule):
        """ Empêche le véhicule de sortir de l'écran et arrête sa vitesse. """
        for point in [vehicule.r_Ar, vehicule.r_Avg, vehicule.r_Avd]:
            if point[0] < 10 or point[0] > LARGEUR - 10  or point[1] < 10 or point[1] > HAUTEUR - 10 :
                vehicule.arret()
                return


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
    distance_obstacle = vehicule.mesurer_distance_obstacle(environnement, tmp)
    print(f"🔍 Distance obstacle : {distance_obstacle} px")
    
    # Gestion des contrôles utilisateur
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        vehicule.tourner("droite")

    elif keys[pygame.K_LEFT]:
        vehicule.tourner("gauche")
            
    if keys[pygame.K_UP]:
        vehicule.acceleration(0.2)       
            
    elif keys[pygame.K_DOWN]:
        vehicule.deceleration(0.2)
            
    if keys[pygame.K_SPACE]:
        vehicule.arret()
        
    if keys[pygame.K_r]:
        vehicule.restart()

    print(f"distance de l'obstacle :{vehicule.mesurer_distance_obstacle(environnement, tmp)}", end = "\r" ) 

    if in_limite(vehicule):
        vehicule.bouger(environnement, tmp)
        rester_dans_limites(vehicule)
    else:
        vehicule.restart()




    # Affichage
    screen.fill(BLANC)
    afficher(screen, vehicule, ROUGE, NOIR, tmp)
    pygame.display.flip()
    clock.tick(60)