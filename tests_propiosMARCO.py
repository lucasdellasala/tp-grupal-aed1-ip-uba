import unittest
from buscaminas import *
from validaciones import *


class test_colocar_minas(unittest.TestCase):
    # Mantener dimensiones
    def test_mantiene_las_dimensiones(self):
        filas, columnas = 2,7
        tablero = colocar_minas(filas, columnas, 3)
        mantiene_el_alto = len(tablero) == filas
        mantiene_el_ancho = len(tablero[0]) == columnas
        self.assertTrue(mantiene_el_alto and mantiene_el_ancho and es_matriz(tablero))
    
    # Cantidad de minas correcta
    def test_cantidad_correcta_de_minas(self):
        tablero = colocar_minas(3,3,2)
        self.assertEqual(cantidad_de_minas(tablero), 2)
    
    def test_cantidad_correcta_de_minas_sin_minas(self):
        tablero = colocar_minas(10,10,0)
        self.assertEqual(cantidad_de_minas(tablero), 0)
    
    def test_cantidad_correcta_de_minas_tablero_lleno_de_minas(self):
        tablero = colocar_minas(2,2,4)
        self.assertEqual(cantidad_de_minas(tablero), 4)
    
    # Los valores del tablero son -1 o 0
    def test_valores_correctos(self):
        tablero = colocar_minas(10,10,10)
        for fila in tablero:
            for casilla in fila:
                self.assertIn(casilla, (-1,0))
    

class test_calcular_numeros(unittest.TestCase):
    def test_minas_en_bordes(self):
        tablero_prueba: list[list[int]] = [[0, -1, 0, 0],
                                           [-1, 0, 0, -1],
                                           [0, -1, -1, -1]]
        tablero_esperado: list[list[int]] = [[2, -1, 2, 1],
                                             [-1, 4, 5, -1], 
                                             [2, -1, -1, -1]]
        calcular_numeros(tablero_prueba)
        self.assertEqual(tablero_prueba, tablero_esperado)

    def test_tablero_sin_minas(self):
        tablero_sin_minas: list[list[int]] = [[0, 0, 0],
                                              [0, 0, 0],
                                              [0, 0, 0]]
        calcular_numeros(tablero_sin_minas)
        self.assertEqual(tablero_sin_minas, [[0, 0, 0],
                                             [0, 0, 0],
                                             [0, 0, 0]])
        
    def test_tablero_lleno(self):
        tablero_lleno: list[list[int]] = [[-1, -1, -1],
                                          [-1, -1, -1],
                                          [-1, -1, -1]]
        calcular_numeros(tablero_lleno)
        self.assertEqual(tablero_lleno, [[-1, -1, -1],
                                         [-1, -1, -1],
                                         [-1, -1, -1]])
        
    def test_bordes_despejados(self):
        tablero_bordes_despejados: list[list[int]] = [[0, 0, 0, 0, 0],
                                                      [0, -1, -1, -1, 0],
                                                      [0, -1, 0, -1, 0],
                                                      [0, -1, -1, -1, 0],
                                                      [0, 0, 0, 0, 0]]
        tablero_esperado: list[list[int]] = [[1, 2, 3, 2, 1],
                                             [2, -1, -1, -1, 2],
                                             [3, -1, 8, -1, 3],
                                             [2, -1, -1, -1, 2],
                                             [1, 2, 3, 2, 1]]
        calcular_numeros(tablero_bordes_despejados)
        self.assertEqual(tablero_bordes_despejados, tablero_esperado)
        

class test_crear_juego(unittest.TestCase):
    def test_estructura_valida(self):
        estado_juego = crear_juego(10,10,10)
        self.assertTrue(estructura_y_tipos_validos(estado_juego))


class tests_descubrir_celda(unittest.TestCase):
    def test_descubrir_celda_igual_a_cero(self):
        tablero_prueba: list[list[int]] = [[2, -1, 2, -1], 
                                           [-1, 3, 2, 1], 
                                           [-1, 2, 0, 0],
                                           [1, 1, 0, 0]]
        tablero_visible_prueba: list[list[str]] = [[VACIO, VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO, VACIO],
                                                   [VACIO, VACIO, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 2, 2)
        self.assertEqual(tablero_visible_prueba, [[' ', ' ', ' ', ' '], 
                                                  ['🏳', '3', '2', '1'], 
                                                  ['🏳', '2', '0', '0'],
                                                  [' ', '1', '0', '0']])
        self.assertEqual(estado_prueba["juego_terminado"], False)
        
    def test_descubrir_celda_distinta_de_cero(self):
        tablero_prueba: list[list[int]] = [[2, -1, 1], 
                                           [-1, 3, 1], 
                                           [-1, 2, 0]]
        tablero_visible_prueba: list[list[str]] = [[VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 1, 1)
        self.assertEqual(tablero_visible_prueba, [[' ', ' ', ' '], 
                                                  ['🏳', '3', ' '], 
                                                  ['🏳', ' ', ' ']])
        self.assertEqual(estado_prueba["juego_terminado"], False)
        
    def test_descubrir_ultima_celda_segura(self):
        tablero_prueba: list[list[int]] = [[2, -1, 2, -1], 
                                           [-1, 3, 2, 1], 
                                           [-1, 2, 0, 0],
                                           [1, 1, 0, 0]]
        tablero_visible_prueba: list[list[str]] = [['2', BANDERA, '2', BANDERA], 
                                                   [BANDERA, VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO, VACIO],
                                                   ['1', VACIO, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 2, 2)
        self.assertEqual(tablero_visible_prueba, [['2', '🏳', '2', '🏳'], 
                                                  ['🏳', '3', '2', '1'], 
                                                  ['🏳', '2', '0', '0'],
                                                  ['1', '1', '0', '0']])
        self.assertEqual(estado_prueba["juego_terminado"], True)

    def test_descubrir_campo_de_ceros_1(self): # PROBLEMA
        tablero_prueba: list[list[int]] = [[-1, 2, 0, 1, -1, 1], 
                                           [-1, 3, 0, 1, 1, 1], 
                                           [-1, 2, 0, 0, 0, 0],
                                           [1, 1, 0, 0, 0, 0]]
        tablero_visible_prueba: list[list[str]] = [[VACIO, VACIO, VACIO, VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO, VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO, VACIO, VACIO, VACIO],
                                                   [VACIO, VACIO, VACIO, VACIO, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 1, 2)
        self.assertEqual(tablero_visible_prueba, [[' ', '2', '0', '1', ' ', ' '], 
                                                  ['🏳', '3', '0', '1', '1', '1'], 
                                                  ['🏳', '2', '0', '0', '0', '0'],
                                                  [' ', '1', '0', '0', '0', '0']])
        self.assertEqual(estado_prueba["juego_terminado"], False)
    
    def test_tablero_no_cambia(self):
        tablero_prueba: list[list[int]] = [[2, -1, 1], 
                                           [-1, 3, 1], 
                                           [-1, 2, 0]]
        tablero_visible_prueba: list[list[str]] = [[VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 2, 2)
        self.assertEqual(tablero_prueba, [[2, -1, 1], 
                                          [-1, 3, 1], 
                                          [-1, 2, 0]])
        
    def test_descubrir_celda_bomba(self):
        tablero_prueba: list[list[int]] = [[2, -1, 1], 
                                           [-1, 3, 1], 
                                           [-1, 2, 0]]
        tablero_visible_prueba: list[list[str]] = [[VACIO, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO], 
                                                   [BANDERA, VACIO, VACIO]]
        estado_prueba: EstadoJuego = {
            "filas" : 3,
            "columnas" : 3,
            "minas" : 3,
            "juego_terminado" : False,
            "tablero" : tablero_prueba,
            "tablero_visible" : tablero_visible_prueba
        }
        descubrir_celda(estado_prueba, 0, 1)
        self.assertEqual(tablero_visible_prueba, [[VACIO, BOMBA, VACIO], 
                                                  [BOMBA, VACIO, VACIO], 
                                                  [BOMBA, VACIO, VACIO]])
        self.assertEqual(estado_prueba["juego_terminado"], True)


if __name__ == '__main__':
    unittest.main(verbosity=2)