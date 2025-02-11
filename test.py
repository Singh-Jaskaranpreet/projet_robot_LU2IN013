import unittest
import math as m
from environnement import Environnement
from vehicule import Vehicule
import time

class TestEnvironnement(unittest.TestCase):

    def setUp(self):
        """Initialisation des objets nécessaires pour les tests."""
        self.env = Environnement()
        self.vehicule = self.env.vehicule

    def test_initialisation(self):
        """Teste l'initialisation de l'environnement."""
        self.assertEqual(self.env.largeur, 1200)
        self.assertEqual(self.env.hauteur, 800)
        self.assertIsInstance(self.env.vehicule, Vehicule)
        self.assertEqual(len(self.env.objects), 1)  # Vérifie qu'il y a un objet par défaut

    def test_segments_intersect(self):
        """Teste la détection d'intersection entre deux segments."""
        # Segments qui s'intersectent
        seg1 = ((0, 0), (10, 10))
        seg2 = ((0, 10), (10, 0))
        self.assertTrue(self.env.segments_intersect(seg1, seg2))

        # Segments qui ne s'intersectent pas
        seg3 = ((0, 0), (10, 0))
        seg4 = ((5, 5), (5, 10))
        self.assertFalse(self.env.segments_intersect(seg3, seg4))

    def test_collision(self):
        """Teste la détection de collision."""
        # Pas de collision initialement
        self.vehicule.p_centre = [200, 400]
        self.assertFalse(self.env.collision())

        # Collision avec un objet
        self.vehicule.p_centre = [500, 500]
        self.assertTrue(self.env.collision())

    def test_correction_apres_collision(self):
        """Teste la correction de la position après une collision."""
        # Simuler une collision
        self.vehicule.p_centre = [500, 500]
        collision = self.env.collision()
        self.env.correction_apres_collision(collision)
        self.assertNotEqual(self.vehicule.p_centre, [500, 500])

    def test_rester_dans_limites(self):
        """Teste que le véhicule reste dans les limites de l'environnement."""
        # Simuler le véhicule hors des limites
        self.vehicule.p_centre = [1201, 400]
        self.env.rester_dans_limites()
        self.assertEqual(self.vehicule.vit_Rd, 0)
        self.assertEqual(self.vehicule.vit_Rg, 0)

    def test_bouger(self):
        """Teste le déplacement du véhicule."""
        initial_position = self.vehicule.p_centre.copy()
        self.vehicule.vit_Rd = 10
        self.vehicule.vit_Rg = 10

        # Simuler un temps écoulé
        self.vehicule.temps.get_temps_ecoule = lambda: 0.1  # Simuler 0.1 seconde

        self.env.bouger()
        self.assertNotEqual(self.vehicule.p_centre, initial_position)

    def test_restart(self):
        """Teste la réinitialisation du véhicule."""
        self.vehicule.p_centre = [500, 500]
        self.vehicule.angle = 45
        self.vehicule.vit_Rd = 10
        self.vehicule.vit_Rg = 10
        self.env.restart()
        self.assertEqual(self.vehicule.p_centre, [self.vehicule.starting_point_x, self.vehicule.starting_point_y])
        self.assertEqual(self.vehicule.angle, 0)
        self.assertEqual(self.vehicule.vit_Rd, 0)
        self.assertEqual(self.vehicule.vit_Rg, 0)

    def test_add_objet(self):
        """Teste l'ajout d'un objet dans l'environnement."""
        initial_length = len(self.env.objects)
        new_object = [(100, 100), (200, 100), (200, 200), (100, 200)]
        self.env.add_objet(new_object)
        self.assertEqual(len(self.env.objects), initial_length + 1)

    def test_position_des_roues(self):
        """Teste le calcul des positions des roues."""
        positions = self.env.position_des_roues(self.vehicule.p_centre)
        self.assertEqual(len(positions), 3)  # Vérifie qu'il y a 3 points (roues)
        for point in positions:
            self.assertEqual(len(point), 2)  # Vérifie que chaque point a 2 coordonnées (x, y)

if __name__ == '__main__':
    unittest.main()