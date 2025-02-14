import pygame
from environnement import *
#LARGEUR, HAUTEUR = 1200, 800

class Affichage:
    # Dimensions de la fenêtre
    def __init__(self,largeur,hauteur):
         self.largeur=largeur
         self.hauteur=hauteur
         self.screen = pygame.display.set_mode((largeur,hauteur))
         self.couleurs = [(255,255,255),(0,0,0),(255,0,0)] #Blanc,Noir,Rouge
        #pygame.display.set_caption("Simulation de Véhicule")



    def afficher(self, objects, environnement):
            """
            Affiche l'environnement, y compris le véhicule, les objets (obstacles),
            et la vitesse du véhicule.
            """

            self.screen.fill(self.couleurs[0]) # Remplir l'écran en blanc

            # Afficher le véhicule sous forme de triangle
            points_triangle = environnement.vehicule.position_des_roues(environnement.vehicule.p_centre)
            pygame.draw.polygon(self.screen, self.couleurs[2], points_triangle)

            # Dessiner la roue arrière
            pygame.draw.circle(self.screen, (0, 0, 0), (int(points_triangle[0][0]), int(points_triangle[0][1])), 3)

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
                self.screen.blit(surface_roue, rect.topleft)

            # Afficher les objets (obstacles)
            for obj in objects:
                pygame.draw.polygon(self.screen, (0, 0, 0), obj)


            # Afficher la vitesse du véhicule à l'écran
            font = pygame.font.SysFont(None, 36)
            vitesse_text = font.render(f"Vitesse: {round(abs((abs(environnement.vehicule.vit_Rd)+abs(environnement.vehicule.vit_Rg))/2), 3)} pixel/s", True, self.couleurs[2])
            self.screen.blit(vitesse_text, (10, 10))
            distance = font.render(f"Distance:{environnement.vehicule.get_distance(environnement)} pixel", True, self.couleurs[2])
            self.screen.blit(distance, (10, 40))
            vitesse = font.render(f"vitesse droite = {environnement.vehicule.vit_Rd}, vitesse gauche {environnement.vehicule.vit_Rg}", True, self.couleurs[2])
            self.screen.blit(vitesse, (10, 770))
            pygame.display.flip() # Met à jour l'écran

    # Fonction pour afficher les instructions
    def afficher_instructions(self):
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
    
        self.screen.fill(self.couleurs[0])  # Remplir l'écran en blanc
        y_offset = 20 # Position de départ pour l'affichage des instructions
        
        for line in instructions:
            text = font.render(line, True, self.couleurs[2])
            self.screen.blit(text, (self.largeur // 4, y_offset))  # Affiche chaque ligne de texte
            y_offset += 100  # Espacement entre les lignes
        
        pygame.display.flip()  # Met à jour l'écran
