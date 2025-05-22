# ---------------------------------------------------------------
# Universidad: Universidad del Valle de Guatemala
# Curso: Algoritmos y Estructuras de Datos
# Nombre: Javier Alvarado, Juan Montenegro
# Carné: 24545, 24750
# Fecha: 21/05/2025
# Descripción: Pruebas unitarias para la clase Grafo del programa
# de rutas entre ciudades con diferentes climas.
# ---------------------------------------------------------------

import unittest
from HT10 import Grafo

class TestGrafo(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba: crea un grafo de ejemplo
        self.g = Grafo()
        self.g.agregar_conexion("A", "B", [5, 6, 7, 8])
        self.g.agregar_conexion("B", "C", [3, 4, 5, 6])
        self.g.floyd_warshall()

    def test_ruta_mas_corta(self):
        # Prueba la ruta más corta entre A y C
        dist, ruta = self.g.ruta_mas_corta("A", "C")
        self.assertEqual(dist, 8)
        self.assertEqual(ruta, ["A", "B", "C"])

    def test_centro_grafo(self):
        # Prueba el cálculo del centro del grafo
        centro = self.g.centro_grafo()
        self.assertEqual(centro, "B")

    def test_interrupcion(self):
        # Prueba la interrupción de una conexión y su efecto en las rutas
        self.g.interrumpir_conexion("A", "B")
        self.g.floyd_warshall()
        dist, ruta = self.g.ruta_mas_corta("A", "C")
        self.assertIsNone(dist)
        self.assertEqual(ruta, [])

if __name__ == "__main__":
    # Ejecuta las pruebas unitarias
    unittest.main()