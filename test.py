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

if __name__ == '__main__':
    unittest.main()