import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127988)  # simbolo de bandera
VACIO = " "  # simbolo vacio inicial

BOMBA_CODIGO = -1
BANDERA_CODIGO = -2
VACIO_CODIGO = 0

TABLERO_FILE = "tablero.txt"
TABLERO_VISIBLE_FILE = "tablero_visible.txt"

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]


def existe_archivo(ruta_directorio: str, nombre_archivo: str) -> bool:
    """
    Verifica si existe un archivo en la ruta especificada.

    Args:
        ruta_directorio (str): La ruta del directorio donde buscar el archivo
        nombre_archivo (str): El nombre del archivo a verificar

    Returns:
        bool: True si el archivo existe, False en caso contrario
    """
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


def crear_tablero_visible(filas: int, columnas: int, codigo: int | str) -> list[list[int]]:
    """
    Crea una matriz de dimensiones especificadas inicializada con un valor dado.

    Args:
        filas (int): Número de filas de la matriz
        columnas (int): Número de columnas de la matriz
        codigo (int | str): Valor con el que se inicializarán todas las celdas

    Returns:
        list[list[int]]: Matriz creada con las dimensiones especificadas
    """
    tablero: list[list[int]] = []
    for fila in range(filas):
        tablero.append([])
        for _ in range(columnas):
            tablero[fila].append(codigo)

    return tablero

# 💥 EJERCICIO  1


def colocar_minas(filas: int, columnas: int, minas: int) -> list[list[int]]:
    """
    Crea un tablero con minas colocadas en posiciones aleatorias.

    Args:
        filas (int): Número de filas del tablero
        columnas (int): Número de columnas del tablero
        minas (int): Número de minas a colocar en el tablero

    Returns:
        list[list[int]]: Tablero con las minas colocadas (BOMBA_CODIGO = -1)
    """
    contador_minas: int = 0
    posiciones_minas: list[int] = random.sample(
        range(0, filas * columnas), minas)
    tablero: list[list[int]] = crear_tablero_visible(
        filas, columnas, VACIO_CODIGO)

    while contador_minas < minas:
        indice_mina: int = posiciones_minas[contador_minas]
        fila: int = indice_mina // columnas
        columna: int = indice_mina % columnas
        tablero[fila][columna] = BOMBA_CODIGO
        contador_minas += 1

    return tablero


def es_bomba(tablero: list[list[int]], indice_fila: int, indice_celda: int) -> bool:
    """
    Verifica si una celda específica contiene una bomba.

    Args:
        tablero (list[list[int]]): El tablero del juego
        indice_fila (int): Índice de la fila a verificar
        indice_celda (int): Índice de la columna a verificar

    Returns:
        bool: True si la celda contiene una bomba, False en caso contrario
    """
    fila_dentro_de_limites: bool = 0 <= indice_fila < len(tablero)
    if not fila_dentro_de_limites:
        return False

    columna_dentro_de_limites: bool = 0 <= indice_celda < len(
        tablero[indice_fila])
    if not columna_dentro_de_limites:
        return False

    return tablero[indice_fila][indice_celda] == BOMBA_CODIGO


def actualizar_contador(tablero: list[list[int]], indice_fila: int, indice_celda: int) -> int:
    """
    Cuenta el número de minas adyacentes a una celda específica.

    Args:
        tablero (list[list[int]]): El tablero del juego
        indice_fila (int): Índice de la fila de la celda
        indice_celda (int): Índice de la columna de la celda

    Returns:
        int: Número de minas adyacentes a la celda especificada
    """
    contador_actualizado: int = 0
    desplazamientos_fila: list[int] = [-1, 0, 1]
    desplazamientos_columna: list[int] = [-1, 0, 1]

    for df in desplazamientos_fila:
        for dc in desplazamientos_columna:
            if df == 0 and dc == 0:
                # celda actual
                continue
            if es_bomba(tablero, indice_fila + df, indice_celda + dc):
                contador_actualizado += 1

    return contador_actualizado

# 💥 EJERCICIO  2


def calcular_numeros(tablero: list[list[int]]) -> None:
    """
    Calcula los números que indican la cantidad de minas adyacentes para cada celda.

    Args:
        tablero (list[list[int]]): El tablero con las minas colocadas

    Returns:
        None: Modifica el tablero in-place
    """
    for indice_fila in range(len(tablero)):
        for indice_celda in range(len(tablero[indice_fila])):
            if tablero[indice_fila][indice_celda] == BOMBA_CODIGO:
                continue

            contador_minas_limitrofes = actualizar_contador(
                tablero, indice_fila, indice_celda)
            tablero[indice_fila][indice_celda] = contador_minas_limitrofes

# 💥 EJERCICIO  3


def crear_juego(filas: int, columnas: int, minas: int) -> EstadoJuego:
    """
    Crea un nuevo estado de juego del buscaminas.

    Args:
        filas (int): Número de filas del tablero
        columnas (int): Número de columnas del tablero
        minas (int): Número de minas en el tablero

    Returns:
        EstadoJuego: Diccionario con el estado inicial del juego
    """
    tablero: list[list[int]] = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)

    res: EstadoJuego = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "tablero_visible": crear_tablero_visible(filas, columnas, VACIO),
        "juego_terminado": False,
        "tablero": tablero
    }

    return res


def copiar_matriz(tablero: list[list[str]]) -> list[list[str]]:
    """
    Crea una copia profunda de una matriz.

    Args:
        tablero (list[list[str]]): La matriz a copiar

    Returns:
        list[list[str]]: Una copia independiente de la matriz original
    """
    copia_del_tablero: list[list[str]] = []
    for filas in tablero:
        copia_del_tablero.append(filas.copy())
    return copia_del_tablero

# 💥 EJERCICIO  4


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """
    Obtiene una copia del tablero visible actual.

    Args:
        estado (EstadoJuego): El estado actual del juego

    Returns:
        list[list[str]]: Una copia del tablero visible
    """
    return copiar_matriz(estado["tablero_visible"])


def posicion_valida(estado: EstadoJuego, fila: int, columna: int) -> bool:
    """
    Verifica si una posición está dentro de los límites del tablero.

    Args:
        estado (EstadoJuego): El estado actual del juego
        fila (int): Índice de la fila a verificar
        columna (int): Índice de la columna a verificar

    Returns:
        bool: True si la posición es válida, False en caso contrario
    """
    return (
        0 <= fila < estado["filas"]
        and 0 <= columna < estado["columnas"]
    )

# 💥 EJERCICIO  5


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Marca o desmarca una celda con una bandera.

    Args:
        estado (EstadoJuego): El estado actual del juego
        fila (int): Índice de la fila de la celda
        columna (int): Índice de la columna de la celda

    Returns:
        None: Modifica el estado in-place
    """
    if estado["juego_terminado"]:
        return

    if not posicion_valida(estado, fila, columna):
        return

    if estado["tablero_visible"][fila][columna] == VACIO:
        estado["tablero_visible"][fila][columna] = BANDERA
    elif estado["tablero_visible"][fila][columna] == BANDERA:
        estado["tablero_visible"][fila][columna] = VACIO


def mostrar_bombas(estado: EstadoJuego) -> None:
    """
    Revela todas las bombas en el tablero visible.

    Args:
        estado (EstadoJuego): El estado actual del juego

    Returns:
        None: Modifica el estado in-place
    """
    for fila in range(estado["filas"]):
        for columna in range(estado["columnas"]):
            if estado["tablero"][fila][columna] == BOMBA_CODIGO:
                estado["tablero_visible"][fila][columna] = BOMBA

# 💥 EJERCICIO  6


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    """
    Descubre una celda del tablero, revelando su contenido.

    Args:
        estado (EstadoJuego): El estado actual del juego
        fila (int): Índice de la fila de la celda
        columna (int): Índice de la columna de la celda

    Returns:
        None: Modifica el estado in-place
    """
    if estado["juego_terminado"]:
        return
    if not posicion_valida(estado, fila, columna):
        return

    if estado["tablero_visible"][fila][columna] == BANDERA:
        return
    if estado["tablero_visible"][fila][columna] != VACIO:
        return

    if estado["tablero"][fila][columna] == BOMBA_CODIGO:
        estado["juego_terminado"] = True
        mostrar_bombas(estado)
        return

    if estado["tablero"][fila][columna] == 0:
        estado["tablero_visible"][fila][columna] = "0"
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                nueva_fila = fila + df
                nueva_columna = columna + dc
                if posicion_valida(estado, nueva_fila, nueva_columna):
                    descubrir_celda(estado, nueva_fila, nueva_columna)
    else:
        estado["tablero_visible"][fila][columna] = str(
            estado["tablero"][fila][columna])

    if verificar_victoria(estado):
        estado["juego_terminado"] = True


def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """
    Verifica si todas las celdas seguras (sin minas) han sido descubiertas.

    Args:
        tablero (list[list[int]]): El tablero con las minas y números
        tablero_visible (list[list[str]]): El tablero visible para el jugador

    Returns:
        bool: True si todas las celdas seguras están descubiertas, False en caso contrario
    """
    for fila in range(len(tablero)):
        for columna in range(len(tablero[fila])):
            if tablero[fila][columna] != BOMBA_CODIGO:  # Si no es bomba
                if tablero_visible[fila][columna] == VACIO:
                    return False
    return True

# 💥 EJERCICIO  7


def verificar_victoria(estado: EstadoJuego) -> bool:
    """
    Verifica si el jugador ha ganado el juego.

    Args:
        estado (EstadoJuego): El estado actual del juego

    Returns:
        bool: True si el jugador ha ganado, False en caso contrario
    """
    return todas_celdas_seguras_descubiertas(estado["tablero"], estado["tablero_visible"])

# 💥 EJERCICIO  8


def reiniciar_juego(estado: EstadoJuego) -> None:
    """
    Reinicia el juego con las mismas dimensiones y número de minas.

    Args:
        estado (EstadoJuego): El estado actual del juego

    Returns:
        None: Modifica el estado in-place
    """
    filas: int = estado["filas"]
    columnas: int = estado["columnas"]
    minas: int = estado["minas"]
    nuevo_estado: EstadoJuego = crear_juego(filas, columnas, minas)
    estado.update(nuevo_estado)


def procesar_linea_tablero(linea: str) -> tuple[bool, list[int]]:
    """
    Procesa una línea del archivo tablero.txt y retorna una tupla (éxito, lista de enteros).
    Si la línea es inválida, retorna (False, []).

    Args:
        linea (str): La línea del archivo a procesar

    Returns:
        tuple[bool, list[int]]: Tupla con (éxito, lista de enteros procesados)
    """
    fila: list[int] = []
    num: str = ""
    i: int = 0
    while i < len(linea):
        if linea[i] == ',':
            if not es_numero(num):
                return False, []
            fila.append(int(num))
            num = ""
        elif linea[i] != '\n':
            num += linea[i]
        i += 1
    if not es_numero(num):
        return False, []
    fila.append(int(num))
    return True, fila


def procesar_linea_tablero_visible(linea: str) -> tuple[bool, list[str]]:
    """
    Procesa una línea del archivo tablero_visible.txt y retorna una tupla (éxito, lista de strings).
    Si la línea es inválida, retorna (False, []).

    Args:
        linea (str): La línea del archivo a procesar

    Returns:
        tuple[bool, list[str]]: Tupla con (éxito, lista de strings procesados)
    """
    fila = []
    num = ""
    i = 0
    while i < len(linea):
        if linea[i] == ',':
            if num == '*':
                fila.append(BANDERA)
            elif num == '?':
                fila.append(VACIO)
            elif not es_numero(num):
                return False, []
            else:
                fila.append(num)
            num = ""
        elif linea[i] != '\n':
            num += linea[i]
        i += 1
    if num == '*':
        fila.append(BANDERA)
    elif num == '?':
        fila.append(VACIO)
    elif not es_numero(num):
        return False, []
    else:
        fila.append(num)
    return True, fila


def validar_dimensiones(tablero: list[list], filas: int, columnas: int) -> bool:
    """
    Valida que el tablero tenga las dimensiones correctas.

    Args:
        tablero (list[list]): El tablero a validar
        filas (int): Número esperado de filas
        columnas (int): Número esperado de columnas

    Returns:
        bool: True si las dimensiones son correctas, False en caso contrario
    """
    if len(tablero) != filas:
        return False
    for fila in tablero:
        if len(fila) != columnas:
            return False
    return True


def validar_tablero_visible(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:
    """
    Valida que el tablero visible sea consistente con el tablero.

    Args:
        tablero (list[list[int]]): El tablero con las minas y números
        tablero_visible (list[list[str]]): El tablero visible para el jugador

    Returns:
        bool: True si el tablero visible es consistente, False en caso contrario
    """
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero_visible[i][j] != BANDERA and tablero_visible[i][j] != VACIO:
                if tablero[i][j] != -1 and str(tablero_visible[i][j]) != str(tablero[i][j]):
                    return False
    return True


def contar_minas(tablero: list[list[int]]) -> int:
    """
    Cuenta la cantidad de minas en el tablero.

    Args:
        tablero (list[list[int]]): El tablero a analizar

    Returns:
        int: Número total de minas en el tablero
    """
    return sum(1 for fila in tablero for celda in fila if celda == -1)

# 💥 EJERCICIO  9


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    """
    Guarda el estado del juego en dos archivos: tablero.txt y tablero_visible.txt.
    Si el juego está terminado o la ruta no existe, no se guarda nada.

    Args:
        estado (EstadoJuego): El estado del juego a guardar
        ruta_directorio (str): La ruta del directorio donde guardar los archivos

    Returns:
        None: No devuelve nada
    """
    if estado["juego_terminado"]:
        return

    if not existe_archivo(ruta_directorio, ""):
        return

    # Guardar tablero
    f_tablero = open(os.path.join(ruta_directorio, TABLERO_FILE), "w")
    lineas_tablero: list[str] = []
    for fila in estado["tablero"]:
        linea = ",".join(str(valor) for valor in fila)
        lineas_tablero.append(linea + "\n")
    f_tablero.writelines(lineas_tablero)
    f_tablero.close()

    # Guardar tablero visible
    tablero_visible_para_guardar = copiar_matriz(estado["tablero_visible"])
    f_visible = open(os.path.join(ruta_directorio, TABLERO_VISIBLE_FILE), "w")
    lineas_visible: list[str] = []
    for fila in tablero_visible_para_guardar:
        valores = []
        for valor in fila:
            if valor == BANDERA:
                valores.append("*")
            elif valor == VACIO:
                valores.append("?")
            else:
                valores.append(str(valor))
        linea = ",".join(valores)
        lineas_visible.append(linea + "\n")
    f_visible.writelines(lineas_visible)
    f_visible.close()


def es_numero(s: str) -> bool:
    """
    Verifica si una cadena es un número válido.

    Args:
        s (str): La cadena a verificar

    Returns:
        bool: True si la cadena representa un número válido, False en caso contrario
    """
    if len(s) == 0:  # ""
        return False
    i = 0
    if s[0] == '-':  # "-..."
        if len(s) == 1:  # "-"
            return False
        i = 1
    while i < len(s):
        if s[i] < '0' or s[i] > '9':
            return False
        i += 1
    return True

# 💥 EJERCICIO  10


def cargar_estado(estado: EstadoJuego, ruta: str) -> bool:
    """
    Carga el estado del juego desde los archivos tablero.txt y tablero_visible.txt.
    Retorna True si se cargó correctamente, False en caso contrario.

    Args:
        estado (EstadoJuego): El estado del juego donde cargar los datos
        ruta (str): La ruta del directorio donde están los archivos

    Returns:
        bool: True si se cargó correctamente, False en caso contrario
    """
    ruta_tablero = os.path.join(ruta, TABLERO_FILE)
    ruta_visible = os.path.join(ruta, TABLERO_VISIBLE_FILE)

    if not existe_archivo(ruta, TABLERO_FILE) or not existe_archivo(ruta, TABLERO_VISIBLE_FILE):
        return False

    f_tablero = open(ruta_tablero, "r")
    tablero: list[str] = f_tablero.readlines()
    f_tablero.close()

    f_visible = open(ruta_visible, "r")
    tablero_visible: list[str] = f_visible.readlines()
    f_visible.close()

    if len(tablero) != len(tablero_visible):
        return False

    tablero_procesado: list[list[int]] = []
    for linea in tablero:
        exito, fila = procesar_linea_tablero(linea)
        if not exito:
            return False
        tablero_procesado.append(fila)

    minas = contar_minas(tablero_procesado)
    if minas == 0:
        return False

    columnas = len(tablero_procesado[0])
    if not validar_dimensiones(tablero_procesado, len(tablero_procesado), columnas):
        return False

    tablero_visible_procesado: list[list[str]] = []
    for linea in tablero_visible:
        exito, fila = procesar_linea_tablero_visible(linea)
        if not exito:
            return False
        tablero_visible_procesado.append(fila)

    if not validar_dimensiones(tablero_visible_procesado, len(tablero_visible_procesado), columnas):
        return False

    if not validar_tablero_visible(tablero_procesado, tablero_visible_procesado):
        return False

    estado["filas"] = len(tablero_procesado)
    estado["columnas"] = columnas
    estado["minas"] = minas
    estado["tablero"] = tablero_procesado
    estado["tablero_visible"] = tablero_visible_procesado
    estado["juego_terminado"] = False

    return True
