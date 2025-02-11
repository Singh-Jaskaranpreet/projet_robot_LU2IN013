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

if __name__ == '__main__':
    unittest.main()