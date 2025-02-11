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

if __name__ == '__main__':
    unittest.main()