import unittest
from buscaminas import (crear_juego, descubrir_celda, marcar_celda, obtener_estado_tablero_visible,
                        reiniciar_juego, colocar_minas, calcular_numeros, verificar_victoria,
                        guardar_estado, cargar_estado, BOMBA, BANDERA, VACIO, EstadoJuego, es_numero,
                        validar_dimensiones, TABLERO_FILE, TABLERO_VISIBLE_FILE)
import os


'''
Ayudamemoria: entre los métodos para testear están los siguientes:

    self.assertEqual(a, b) -> testea que a y b tengan el mismo valor
    self.assertTrue(x)     -> testea que x sea True
    self.assertFalse(x)    -> testea que x sea False
    self.assertIn(a, b)    -> testea que a esté en b (siendo b una lista o tupla)
'''


def cant_minas_en_tablero(tablero: list[list[int]]) -> int:
    """Chequea que el número de minas en el tablero sea igual al número de minas esperado"""
    contador_minas: int = 0
    for fila in tablero:
        for celda in fila:
            if celda == -1:
                contador_minas += 1
    return contador_minas


def son_solo_ceros_y_bombas(tablero: list[list[int]]) -> bool:
    for fila in tablero:
        for celda in fila:
            if celda not in [0, -1]:
                return False
    return True


def dimension_correcta(tablero: list[list[int]], filas: int, columnas: int) -> bool:
    """Chequea que el tablero tenga las dimensiones correctas"""
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True

# Este test es para hacer el setup inicial del CI


class setup_test(unittest.TestCase):
    def test_ejemplo(self):
        self.assertTrue(True)


class colocar_minas_test(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1

        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        # Testeamos que el tablero tenga solo bombas o ceros
        self.assertTrue(son_solo_ceros_y_bombas(tablero))
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(tablero), minas)

    def test_dimension_correcta(self):
        filas = 2
        columnas = 2
        minas = 1
        tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
        self.assertTrue(dimension_correcta(tablero, filas, columnas))


class calcular_numeros_test(unittest.TestCase):
    def test_ejemplo(self):
        tablero = [[0, -1],
                   [0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1, -1],
                                   [1, 1]])

    def test_matriz_grande(self):
        tablero = [[0, 0, 0],
                   [0, -1, 0],
                   [-1, 0, 0]]

        calcular_numeros(tablero)
        # Testeamos que el tablero tenga los números correctos
        self.assertEqual(tablero, [[1, 1, 1],
                                   [2, -1, 1],
                                   [-1, 2, 1]])


class crear_juego_test(unittest.TestCase):
    def test_ejemplo(self):
        filas = 2
        columnas = 2
        minas = 1
        estado: EstadoJuego = crear_juego(filas, columnas, minas)
        # Testeamos que el tablero tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(estado['tablero'], filas, columnas))
        # Testeamos que el tablero visible tenga las dimensiones correctas
        self.assertTrue(dimension_correcta(
            estado['tablero_visible'], filas, columnas))
        # Testeamos que el tablero visible esté vacío
        for fila in estado['tablero_visible']:
            for celda in fila:
                self.assertEqual(celda, VACIO)
        # Testeamos que el resto es lo esperado
        self.assertEqual(estado['filas'], filas)
        self.assertEqual(estado['columnas'], columnas)
        self.assertEqual(estado['minas'], minas)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), minas)


class obtener_estado_tablero_visible_test(unittest.TestCase):
    def test_ejemplo(self):
        mock_tablero_visible: list[list[str]] = [[" ", " "], [" ", " "]]
        estado: EstadoJuego = {
            "filas": 2,
            "columnas": 2,
            "minas": 1,
            "tablero_visible": mock_tablero_visible,
            "juego_terminado": False,
            "tablero": [[1, 1], [-1, 1]]
        }
        tablero_visible = obtener_estado_tablero_visible(estado)
        self.assertEqual(tablero_visible, mock_tablero_visible)


class marcar_celda_test(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        # Testeamos que sólo la celda marcada sea visible
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True
        }
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertTrue(estado['juego_terminado'])

    def test_posicion_invalida(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 3, 3)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_posicion_bandera(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        marcar_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])


class descubrir_celda_test(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [2, -1, 1],
                [-1, 3, 1],
                [-1, 2, 0]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 2, 2)
        # Testeamos que la celda descubierta sea visible
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO, VACIO],
            [VACIO, "3", "1"],
            [VACIO, "2", "0"]
        ])
        # Testeamos que el resto no se modificó
        self.assertEqual(estado['filas'], 3)
        self.assertEqual(estado['columnas'], 3)
        self.assertEqual(estado['minas'], 3)
        self.assertEqual(estado['tablero'], [
            [2, -1, 1],
            [-1, 3, 1],
            [-1, 2, 0]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 3)
        self.assertFalse(estado['juego_terminado'])

    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': True
        }
        descubrir_celda(estado, 0, 0)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertTrue(estado['juego_terminado'])

    def test_posicion_invalida(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 3, 3)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_posicion_bandera(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, VACIO],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)
        self.assertEqual(estado['tablero_visible'], [
            [BANDERA, VACIO],
            [VACIO, VACIO]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_posicion_no_vacio(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 1)
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            ["1", "1"]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertFalse(estado['juego_terminado'])

    def test_posicion_bomba(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 3,
            'tablero': [
                [-1, 2, 1],
                [2, -1, 2],
                [1, 2, -1]
            ],
            'tablero_visible': [
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO],
                [VACIO, VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        descubrir_celda(estado, 0, 0)  # Descubrimos una bomba
        self.assertEqual(estado['tablero_visible'], [
            [BOMBA, VACIO, VACIO],
            [VACIO, BOMBA, VACIO],
            [VACIO, VACIO, BOMBA]
        ])
        self.assertEqual(estado['tablero'], [
            [-1, 2, 1],
            [2, -1, 2],
            [1, 2, -1]
        ])
        self.assertTrue(estado['juego_terminado'])


class verificar_victoria_test(unittest.TestCase):
    def test_victoria_correcta(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                ["1", "1"]
            ],
            'juego_terminado': False
        }
        self.assertTrue(verificar_victoria(estado))

    def test_celda_segura_sin_descubrir(self):
        """Test donde hay una celda segura sin descubrir"""
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, "1"]  # Celda segura sin descubrir
            ],
            'juego_terminado': False
        }
        self.assertFalse(verificar_victoria(estado))

    def test_multiple_celdas_seguras(self):
        """Test con múltiples celdas seguras, todas descubiertas"""
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 3,
            'minas': 2,
            'tablero': [
                [-1, 2, 1],
                [2, -1, 1],
                [1, 1, 0]
            ],
            'tablero_visible': [
                [VACIO, "2", "1"],
                ["2", VACIO, "1"],
                ["1", "1", "0"]
            ],
            'juego_terminado': False
        }
        self.assertTrue(verificar_victoria(estado))


class obtener_estado_tablero_test(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        # Testeamos que el estado del tablero sea el esperado
        self.assertEqual(obtener_estado_tablero_visible(estado), [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        # Testeamos que nada se modificó
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, "1"],
            [VACIO, VACIO]
        ])
        self.assertFalse(estado['juego_terminado'])


class reiniciar_juego_test(unittest.TestCase):
    def test_ejemplo(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }
        reiniciar_juego(estado)
        # Testeamos que el juego esté reiniciado
        self.assertEqual(estado['tablero_visible'], [
            [VACIO, VACIO],
            [VACIO, VACIO]
        ])
        # Testeamos que haya una mina en el tablero
        self.assertEqual(cant_minas_en_tablero(estado['tablero']), 1)
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(len(estado['tablero']), 2)
        self.assertEqual(len(estado['tablero'][0]), 2)
        self.assertFalse(estado['juego_terminado'])
        # Testeamos que es diferente tablero
        self.assertNotEqual(estado['tablero'], [
            [-1, 1],
            [1, 1]
        ])


class guardar_estado_test(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        # Creamos un directorio temporal para las pruebas
        self.test_dir = "test_guardado"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

    def tearDown(self):
        """Limpieza después de cada test"""
        # Eliminamos los archivos creados
        for archivo in [TABLERO_FILE, TABLERO_VISIBLE_FILE]:
            ruta = os.path.join(self.test_dir, archivo)
            if os.path.exists(ruta):
                os.remove(ruta)
        # Eliminamos el directorio temporal
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_ejemplo_especificacion(self):
        """Test que verifica que el guardado coincide exactamente con el ejemplo de la especificación"""
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [VACIO, "1"],
                [VACIO, VACIO]
            ],
            'juego_terminado': False
        }

        guardar_estado(estado, self.test_dir)

        with open(os.path.join(self.test_dir, TABLERO_FILE), "r") as f:
            contenido = f.read().strip()
            self.assertEqual(contenido, "-1,1\n1,1")

        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "r") as f:
            contenido = f.read().strip()
            self.assertEqual(contenido, "?,1\n?,?")

    def test_guardar_estado_valido(self):
        """Test que verifica que se guarda correctamente un estado válido"""
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, "1"],
                [VACIO, "1"]
            ],
            'juego_terminado': False
        }

        guardar_estado(estado, self.test_dir)

        self.assertTrue(os.path.exists(
            os.path.join(self.test_dir, TABLERO_FILE)))
        self.assertTrue(os.path.exists(os.path.join(
            self.test_dir, TABLERO_VISIBLE_FILE)))

        with open(os.path.join(self.test_dir, TABLERO_FILE), "r") as f:
            lineas = f.readlines()
            self.assertEqual(len(lineas), estado['filas'])
            self.assertEqual(lineas[0].strip(), "-1,1")
            self.assertEqual(lineas[1].strip(), "1,1")

        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "r") as f:
            lineas = f.readlines()
            self.assertEqual(len(lineas), estado['filas'])
            self.assertEqual(lineas[0].strip(), "*,1")
            self.assertEqual(lineas[1].strip(), "?,1")

    def test_juego_terminado(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BOMBA, "1"],
                ["1", "1"]
            ],
            'juego_terminado': True
        }

        self.assertFalse(guardar_estado(estado, self.test_dir))

    def test_ruta_invalida(self):
        estado: EstadoJuego = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [
                [-1, 1],
                [1, 1]
            ],
            'tablero_visible': [
                [BANDERA, "1"],
                [VACIO, "1"]
            ],
            'juego_terminado': False
        }

        self.assertFalse(guardar_estado(estado, "ruta/que/no/existe"))

    def test_formato_archivos(self):
        estado: EstadoJuego = {
            'filas': 3,
            'columnas': 4,
            'minas': 2,
            'tablero': [
                [-1, 2, 1, 0],
                [2, -1, 1, 0],
                [1, 1, 0, 0]
            ],
            'tablero_visible': [
                [BANDERA, "2", "1", VACIO],
                ["2", BANDERA, "1", "0"],
                ["1", "1", "0", "0"]
            ],
            'juego_terminado': False
        }

        guardar_estado(estado, self.test_dir)

        with open(os.path.join(self.test_dir, TABLERO_FILE), "r") as f:
            lineas = f.readlines()
            self.assertEqual(len(lineas), estado['filas'])
            for linea in lineas:
                self.assertEqual(linea.count(","), estado['columnas'] - 1)
                self.assertNotIn(" ", linea)

        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "r") as f:
            lineas = f.readlines()
            self.assertEqual(len(lineas), estado['filas'])
            for linea in lineas:
                self.assertEqual(linea.count(","), estado['columnas'] - 1)
                self.assertNotIn(" ", linea)
                self.assertNotIn(BANDERA, linea)
                self.assertNotIn(VACIO, linea)


class cargar_estado_test(unittest.TestCase):
    def setUp(self):
        # Creamos un directorio temporal para las pruebas
        self.test_dir = "test_save"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)

        # Estado inicial para las pruebas
        self.estado_inicial = {
            'filas': 2,
            'columnas': 2,
            'minas': 1,
            'tablero': [[1, 1], [1, 1]],
            'tablero_visible': [[VACIO, VACIO], [VACIO, VACIO]],
            'juego_terminado': False
        }

    def tearDown(self):
        # Limpiamos los archivos de prueba
        archivos = [TABLERO_FILE, TABLERO_VISIBLE_FILE]
        for archivo in archivos:
            ruta = os.path.join(self.test_dir, archivo)
            if os.path.exists(ruta):
                try:
                    os.remove(ruta)
                except:
                    pass  # Ignoramos errores al eliminar archivos

        # Intentamos eliminar el directorio
        if os.path.exists(self.test_dir):
            try:
                os.rmdir(self.test_dir)
            except:
                # Si no podemos eliminar el directorio, intentamos eliminar todo su contenido
                import shutil
                shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_archivos_no_existen(self):
        """Test que verifica que retorne False si no existen los archivos"""
        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_ejemplo_especificacion(self):
        """Test que verifica el ejemplo de la especificación"""
        # Creamos los archivos como en el ejemplo
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        # Estado inicial como en el ejemplo
        estado = {
            'filas': 50,
            'columnas': 15,
            'minas': 150,
            'tablero': [[1, 7], [8, 0]],
            'tablero_visible': [[VACIO, '1'], ['1', '1']],
            'juego_terminado': False
        }

        self.assertTrue(cargar_estado(estado, self.test_dir))

        # Verificamos que el estado se actualizó correctamente
        self.assertEqual(estado['filas'], 2)
        self.assertEqual(estado['columnas'], 2)
        self.assertEqual(estado['minas'], 1)
        self.assertEqual(estado['tablero'], [[-1, 1], [1, 1]])
        self.assertEqual(estado['tablero_visible'], [
                         [BANDERA, '1'], [VACIO, VACIO]])
        self.assertFalse(estado['juego_terminado'])

    def test_cantidad_lineas_incorrecta(self):
        """Test que verifica que retorne False si la cantidad de líneas no coincide con filas"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1\n1,1")  # 3 líneas cuando deberían ser 2
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_cantidad_comas_incorrecta(self):
        """Test que verifica que retorne False si la cantidad de comas no coincide con columnas-1"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1,1\n1,1,1")  # 2 comas cuando deberían ser 1
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_tablero_sin_bombas(self):
        """Test que verifica que retorne False si no hay bombas (-1) en tablero.txt"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("1,1\n1,1")  # No hay bombas
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_tablero_visible_valores_invalidos(self):
        """Test que verifica que retorne False si hay valores inválidos en tablero_visible.txt"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,9\n?,?")  # 9 es inválido (debe ser 0-8)

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_tablero_visible_no_coincide_con_tablero(self):
        """Test que verifica que retorne False si los números en tablero_visible no coinciden con tablero"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,2\n?,?")  # 2 no coincide con 1 en tablero.txt

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_carga_correcta(self):
        """Test que verifica una carga correcta con todos los valores válidos"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertTrue(cargar_estado(self.estado_inicial, self.test_dir))

        # Verificamos que el estado se actualizó correctamente
        self.assertEqual(self.estado_inicial['filas'], 2)
        self.assertEqual(self.estado_inicial['columnas'], 2)
        self.assertEqual(self.estado_inicial['minas'], 1)
        self.assertEqual(self.estado_inicial['tablero'], [[-1, 1], [1, 1]])
        self.assertEqual(self.estado_inicial['tablero_visible'], [
                         [BANDERA, '1'], [VACIO, VACIO]])
        self.assertFalse(self.estado_inicial['juego_terminado'])

    def test_es_numero(self):
        """Test que verifica la función es_numero"""
        self.assertTrue(es_numero("123"))
        self.assertTrue(es_numero("-1"))
        self.assertFalse(es_numero("abc"))
        self.assertFalse(es_numero("12a"))
        self.assertFalse(es_numero(""))

    def test_archivo_tablero_vacio(self):
        """Test que verifica que retorne False si tablero.txt está vacío"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_archivo_tablero_visible_vacio(self):
        """Test que verifica que retorne False si tablero_visible.txt está vacío"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_valor_vacio_entre_comas(self):
        """Test que verifica que retorne False si hay valores vacíos entre comas"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,,1\n1,1")  # Valor vacío entre comas
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_fila_vacia(self):
        """Test que verifica que retorne False si hay una fila vacía"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n\n1,1")  # Fila vacía
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_columnas_diferentes(self):
        """Test que verifica que retorne False si las filas tienen diferente cantidad de columnas"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            # Primera fila tiene 3 columnas, segunda tiene 2
            f.write("-1,1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_columnas_diferentes_visible(self):
        """Test que verifica que retorne False si las filas del tablero visible tienen diferente cantidad de columnas"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            # Primera fila tiene 3 columnas, segunda tiene 2
            f.write("*,1,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_valor_invalido_tablero(self):
        """Test que verifica que retorne False si hay un valor inválido en tablero.txt"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,a\n1,1")  # 'a' no es un número válido
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_valor_invalido_tablero_visible(self):
        """Test que verifica que retorne False si hay un valor inválido en tablero_visible.txt"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("*,a\n?,?")  # 'a' no es un número válido

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_valor_no_numerico_despues_coma_tablero_visible(self):
        """Test que verifica que retorne False si hay un valor no numérico después de una coma en el tablero visible"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            # 'abc' no es un número válido y está después de una coma
            f.write("*,abc,1\n?,?")

        self.assertFalse(cargar_estado(self.estado_inicial, self.test_dir))

    def test_bandera_al_final_de_fila_tablero_visible(self):
        """Test que verifica que se procese correctamente una bandera al final de la fila en tablero_visible.txt"""
        with open(os.path.join(self.test_dir, TABLERO_FILE), "w") as f:
            f.write("-1,1\n1,1")
        with open(os.path.join(self.test_dir, TABLERO_VISIBLE_FILE), "w") as f:
            f.write("1,*\n?,?")  # La bandera está al final de la primera fila

        self.assertTrue(cargar_estado(self.estado_inicial, self.test_dir))
        self.assertEqual(self.estado_inicial['tablero_visible'][0][1], BANDERA)


class es_numero_test(unittest.TestCase):
    def test_es_numero(self):
        self.assertTrue(es_numero("123"))
        self.assertTrue(es_numero("-1"))
        self.assertFalse(es_numero("abc"))
        self.assertFalse(es_numero("12a"))
        self.assertFalse(es_numero("-"))


class validar_dimensiones_test(unittest.TestCase):
    def test_filas_incorrectas(self):
        """Test que verifica que retorne False si el tablero tiene una cantidad de filas diferente a la esperada"""
        tablero = [[1, 1], [1, 1], [1, 1]]  # 3 filas
        self.assertFalse(validar_dimensiones(
            tablero, 2, 2))  # esperamos 2 filas

    def test_columnas_incorrectas(self):
        """Test que verifica que retorne False si alguna fila tiene una cantidad de columnas diferente a la esperada"""
        tablero = [[1, 1, 1], [1, 1]
                   ]  # primera fila tiene 3 columnas, segunda tiene 2
        self.assertFalse(validar_dimensiones(
            tablero, 2, 2))  # esperamos 2 columnas

    def test_dimensiones_correctas(self):
        """Test que verifica que retorne True si las dimensiones son correctas"""
        tablero = [[1, 1], [1, 1]]
        self.assertTrue(validar_dimensiones(tablero, 2, 2))


"""
- Agregar varios casos de prueba para cada función.
- Se debe cubrir al menos el 95% de las líneas de cada función.
- Se debe cubrir al menos el 95% de ramas de cada función.
"""

if __name__ == '__main__':
    unittest.main(verbosity=2)
