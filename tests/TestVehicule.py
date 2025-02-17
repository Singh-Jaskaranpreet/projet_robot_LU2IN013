import unittest
import math as m
from src.modele import Vehicule
import time


class TestVehicule(unittest.TestCase):

    def setUp(self):
        """Initialisation des objets nécessaires pour les tests."""
        self.vehicule = Vehicule("Robot",[200, 400] , 50, 50,self)

    def test_accelerer(self):
        # Test de la fonction accelerer
        self.vehicule.accelerer(50)
        self.assertEqual(self.vehicule.vit_Rg, 50)
        self.assertEqual(self.vehicule.vit_Rd, 50)

        # Test avec une valeur qui dépasse la limite maximale
        self.vehicule.accelerer(200) 
        self.assertEqual(self.vehicule.vit_Rg, 150)
        self.assertEqual(self.vehicule.vit_Rd, 150)

    def test_freiner(self):
        # Initialisation des vitesses
        self.vehicule.vit_Rg = 100
        self.vehicule.vit_Rd = 100

        # Test de la fonction freiner
        self.vehicule.freiner(50)
        self.assertEqual(self.vehicule.vit_Rg, 50)
        self.assertEqual(self.vehicule.vit_Rd, 50)

        # Test avec une valeur qui dépasse la limite minimale
        self.vehicule.freiner(200)
        self.assertEqual(self.vehicule.vit_Rg, 0)
        self.assertEqual(self.vehicule.vit_Rd, 0)

    def test_reculer(self):
        # Test de la méthode reculer
        self.vehicule.reculer(30)
        self.assertEqual(self.vehicule.vit_Rg, -30)
        self.assertEqual(self.vehicule.vit_Rd, -30)

        # Test de la limite inférieure
        self.vehicule.reculer(100)
        self.assertEqual(self.vehicule.vit_Rg, -50)
        self.assertEqual(self.vehicule.vit_Rd, -50)

    def test_position_des_roues(self):
        """Teste le calcul des positions des roues."""
        positions = self.vehicule.position_des_roues(self.vehicule.p_centre)
        self.assertEqual(len(positions), 3)  # Vérifie qu'il y a 3 points (roues)
        for point in positions:
            self.assertEqual(len(point), 2)  # Vérifie que chaque point a 2 coordonnées (x, y)

    def test_set_vrd(self):
        # Test de la méthode set_vrd
        self.vehicule.set_vrd(75)
        self.assertEqual(self.vehicule.vit_Rd, 75)

        # Test de la limite supérieure
        self.vehicule.set_vrd(200)
        #self.assertEqual(self.vehicule.vit_Rd, 200)

        # Test de la limite inférieure
        self.vehicule.set_vrd(-200)
        #self.assertEqual(self.vehicule.vit_Rd, -200)

    def test_set_vrg(self):
        # Test de la méthode set_vrg
        self.vehicule.set_vrg(75)
        self.assertEqual(self.vehicule.vit_Rg, 75)

        # Test de la limite supérieure
        self.vehicule.set_vrg(200)
        self.assertEqual(self.vehicule.vit_Rg, 150)

        # Test de la limite inférieure
        self.vehicule.set_vrg(-200)
        #self.assertEqual(self.vehicule.vit_Rg, 0)

    def test_acr_Rg(self):
        # Test de la méthode acr_Rg
        self.vehicule.acr_Rg(50)
        self.assertEqual(self.vehicule.vit_Rg, 50)

        # Test de la limite supérieure
        self.vehicule.acr_Rg(200)
        self.assertEqual(self.vehicule.vit_Rg, 150)

        # Test de la limite inférieure
        self.vehicule.acr_Rg(-200)
        #self.assertEqual(self.vehicule.vit_Rg, -100)

    def test_acr_Rd(self):
        # Test de la méthode acr_Rd
        self.vehicule.acr_Rd(50)
        self.assertEqual(self.vehicule.vit_Rd, 50)

        # Test de la limite supérieure
        self.vehicule.acr_Rd(200)
        self.assertEqual(self.vehicule.vit_Rd, 150)

        # Test de la limite inférieure
        self.vehicule.acr_Rd(-200)
        #self.assertEqual(self.vehicule.vit_Rd, -100)

if __name__ == '__main__':
    unittest.main()