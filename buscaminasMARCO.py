import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # símbolo de una mina
BANDERA = chr(127987)  # símbolo de bandera blanca
VACIO = " "  # símbolo vacío inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]


def existe_archivo(ruta_directorio: str, nombre_archivo: str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))

"Función de utilidad para todos los ejercicios:"

def es_pos_valida(tablero: list[list[int]], fila: int, columna: int) -> bool:
    """Determina si una posición es valida para un tablero
    Args:
        tablero (list[list[int]]): Matriz para representar el tablero.
        fila (int): Índice a de la fila.
        columna (int): Índice a de la columna.

    Returns:
        bool: True si la posicion es valida, False si es invalida.
    """
    fila_valida: bool = 0 <= fila < len(tablero)
    columna_valida: bool = 0 <= columna < len(tablero[0])
    return fila_valida and columna_valida

# Ejercicio 1.


def convertir_a_matriz_entera(seq: list[int], filas: int, columnas: int) -> list[list[int]]:
    res: list[list[int]] = []

    for indice_fila in range(filas):
        aux: list[int] = []
        for indice_columna in range(columnas):
            posicion = indice_fila * columnas + indice_columna
            aux.append(seq[posicion])
        res.append(aux)
    return res

def convertir_a_matriz_caracteres(seq: list[str], filas: int, columnas: int) -> list[list[str]]:
    res: list[list[str]] = []

    for indice_fila in range(filas):
        aux: list[str] = []
        for indice_columna in range(columnas):
            posicion = indice_fila * columnas + indice_columna
            aux.append(seq[posicion])
        res.append(aux)
    return res

def colocar_minas(filas: int, columnas: int, minas: int) -> list[list[int]]:
    res: list[int] = [-1] * minas + [0] * ((filas * columnas) - minas )
    random.shuffle(res)
    return convertir_a_matriz_entera(res, filas, columnas)


# Ejercicio 2.

def calcular_numeros(tablero: list[list[int]]) -> None:
    """Calcula los números adyacentes a una mina

    Args:
        tablero (list[list[int]]): Matriz que representa el tablero
    
    Returns:
        None: Es un proceso, entonces modifica el tablero que fué pasado por referencia.
    """
    filas: int = len(tablero)
    columnas: int = len(tablero[0])
    # Recorremos todo el tablero buscando buscando todas las posiciones que no tengan una minas
    for i_fila in range(filas):
        for i_col in range(columnas):
            if tablero[i_fila][i_col] != -1:
                tablero[i_fila][i_col] = cantidad_minas_adyacentes(tablero, i_fila, i_col)

    return


def cantidad_minas_adyacentes(tablero: list[list[int]], filas:int, columnas :int) -> int:
    """
    Args:
        tablero (list[list[int]]): Matriz que representa el tablero
        fila (int): Índice de la fila
        columna (int): Índice de la columna

    Returns:
        int: Cantidad de minas adyantes de un casillero.
    """
    contador: int = 0

    "Recorre las filas actual, superior e inferior, y las columnas actual, anterior"
    "y posterior respecto de la posición de entrada (si están en los límites del tablero)."
    "Por cada valor -1, contabiliza una bomba."

    for i_fila in range(filas - 1, filas + 2):
        for i_col in range(columnas - 1, columnas + 2):
            if (es_pos_valida(tablero, i_fila, i_col) and tablero[i_fila][i_col] == -1):
                contador += 1

    return contador


# Ejercicio 3.

def inicializar_tablero_visible(columnas: int, filas: int) -> list[list[str]]:
    """
    Recibe una cantidad de filas y columnas y devuelve un tablero de tales dimensiones
    Args:
        columnas (int): Número de filas del tablero.
        filas (int): Número de columnas del tablero.
    Returns:
        list[list[str]]: Matriz inicial del tablero visible para el jugador.
    """
    
    lista: list[str] = [VACIO]*(columnas * filas)
    
    return convertir_a_matriz_caracteres(lista, filas, columnas)

def crear_juego(filas: int, columnas: int, minas: int) -> EstadoJuego:
    """Inicializa el estado inicial del juego.

    Args:
        filas (int): Cantidad de filas del tablero
        columnas (int): Cantidad de columnas del tablero
        minas (int): Cantidad de minas del tablero

    Returns:
        EstadoJuego: Diccionario con información del juego.
        res = {
            'filas': Número de  filas,
            'columnas': Número de  columnas,
            'minas': Número de  minas,
            'tablero_visible': Matriz[filas x columnas]. 0 <= i <= filas, 0 <= j <= columnas / matriz[i][j] = VACIO
            'juego_terminado': Estado en el que se encuentra el juego   
        }
    """

    tablero = colocar_minas(filas, columnas, minas)
    calcular_numeros(tablero)
    res: EstadoJuego = {
        "filas": filas,
        "columnas": columnas,
        "minas": minas,
        "tablero_visible": inicializar_tablero_visible(columnas, filas),
        "juego_terminado": False,
        "tablero": tablero,
    }

    return res


# Ejercicio 4


def copiar_matriz(tablero: list[list[str]]) -> list[list[str]]:
    """Crea una copia independiente de una matriz compleja.

    Args:
        tablero (list[list[Any]]): Matriz a copir.

    Returns:
        list[list[Any]]: Copia de la matriz original, pero con otro puntero en memoria.
    """
    # Implementación de copia profunda.
    copia_del_tablero: list[list[str]] = []
    for filas in tablero:
        copia_del_tablero.append(filas.copy()) 
    return copia_del_tablero

def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    """Obtiene una copia del estado acutal del juego.
    Args:
        estado (EstadoJuego): Diccionario con el estado del juego.

    Returns:
        list[list[str]]: Copia del tablero visible actual.
    """
    return copiar_matriz(estado['tablero_visible'])

# Ejercicio 5.

def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    if not estado['juego_terminado']: 
        tablero_visible:list[list[str]] = estado['tablero_visible']

        tipo = tablero_visible[fila][columna]

        if tipo == BANDERA:
            tablero_visible[fila][columna] = VACIO
        else:
            tablero_visible[fila][columna] = BANDERA
        
        
# Ejercicio 6.
     
def todas_celdas_seguras_descubiertas(tablero: list[list[int]], tablero_visible: list[list[str]]) -> bool:

    "Recibe un tablero y un tablero visible como parámetros in. Sirve como función auxiliar"
    "a 'descubrir_celda', devolviendo True sí y sólo si todas aquellas celdas en las que no"
    "hay una mina han sido descubiertas por el usuario del juego."

    for i_filas in range(len(tablero)):
        for i_columnas in range(len(tablero[0])):
            celda = tablero[i_filas][i_columnas]
            celda_visible = tablero_visible[i_filas][i_columnas]

            "En cuanto se encuentra un contraejemplo a la condición deseada, es decir, un caso"
            "de celda segura que no fue descubierta, la función termina su ejecución y devuelve False."
            "Si esto nunca sucede, se asume True."

            if celda != -1 and (celda_visible == VACIO or celda_visible == BANDERA): 
                return False
            
    return True

def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    
    "Dadas una fila y una columna válidas en el tablero como parámetros in, y un estado del juego"
    "como parámetro inout, modifica el tablero visible revelándole al usuario información sobre el tablero"
    "de juego, en función de la celda con la que haya interactuado (posición de entrada fila-columna)."
    "Se asume que la celda en cuestión no fue marcada como bandera ni descubierta por el usuario previamente."

    tablero = estado["tablero"]
    tablero_visible = estado["tablero_visible"]

    if not estado["juego_terminado"]:

        # Si se halló una bomba, finaliza el juego y revela todas las bombas restantes:

        if tablero[fila][columna] == -1: 
            estado["juego_terminado"] = True
            for i_fila in range(len(tablero)):
                for i_col in range(len(tablero[0])):
                    if tablero[i_fila][i_col] == -1:
                        tablero_visible[i_fila][i_col] = BOMBA

        # Si no se halló una bomba, descubre las celdas vacías que correspondan
        # (de acuerdo con lo detallado en la función 'caminos_descubiertos')

        else:
            camino = caminos_descubiertos(tablero, tablero_visible, fila, columna)
            for (i_fila, i_col) in camino: 
                tablero_visible[i_fila][i_col] = str(tablero[i_fila][i_col])

            "Si aquellas celdas descubiertas resultaron ser las últimas celdas seguras"
            "de la partida, el juego se da por terminado:"

            if todas_celdas_seguras_descubiertas(tablero, tablero_visible):
                estado["juego_terminado"] = True

def caminos_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], fila: int, columna: int) -> list[tuple[int, int]]:
    
    "Dados los tableros de juego (el oculto y el visible al usuario), una fila y una columna válidas, devuelve una lista"
    "de posiciones comprendidas dentro de los límites del tablero que deberán ser descubiertas. Se separan los siguientes casos:"

    res: list[tuple[int, int]] = [(fila,columna)]  # 'res' se inicializa con la posición de entrada, que en todos los casos será revelada al usuario. 

    "Si la celda en (fila, columna) es alguna rodeada por una o más minas, es decir, de valor mayor a cero, aquella será la única que deba descubrirse:"

    if tablero[fila][columna] > 0 :
        return res
    
    "Si la ejecución continúa, es porque la celda tiene valor igual a cero (no hay minas en sus posiciones adyacentes). En ese caso, corresponde"
    "descubrir todas las celdas inmediatamente vecinas que no hayan sido marcadas con bandera, pues se sabe que son seguras, y si hubiera"
    "otra de igual valor (cero), también se revelarán las que la rodeen, sucesivamente, hasta que no se encuentren más de ellas."

    for (fila_cero, col_cero) in ceros_descubiertos(tablero, tablero_visible, fila, columna):
        vecinos_de_cero: list[tuple[int,int]] = guardar_pos_adyacentes(fila_cero, col_cero, tablero)
        res += vecinos_de_cero

    return res

def ceros_descubiertos(tablero: list[list[int]], tablero_visible: list[list[str]], fila: int, columna: int) -> list[tuple[int, int]]:
    
    "Toma un tablero y un tablero visible asociados a un juego, una fila y una columna como parámetros in."
    "Se asume que la celda marcada por el usuario en la posición (fila,columna) tiene valor cero, y se devuelve una lista"
    "con todas las posiciones, también de valor cero, que corresponde descubrir. Interesa identificar a estas celdas por"
    "separado pues, tienen la particularidad de que si alguna de ellas debe ser descubierta, entonces, todas sus adyacentes también."
    
    res: list[tuple[int,int]] = [(fila,columna)]  # guardará la selección final de posiciones del tablero cuya celda vale cero.

    direcciones = [(-1,-1),(-1,0),(1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]  # contiene los incrementos y decrementos que deberán seguir los iteradores de fila y columna, si se quiere ir en las direcciones vertical, horizontal y diagonales, en todos sus sentidos.
    
    i_res = 0
    while i_res < len(res):
        i_fila, i_col = res[i_res]  # inicializa los índices de fila y columna según la última posición guardada en 'res'.

        "Recorre las posiciones adyacentes a una dada, en las ocho direcciones posibles:"
    
        for direccion_x, direccion_y in direcciones:
            new_cord_fila, new_cord_columna = i_fila + direccion_x, i_col + direccion_y

            "Comprueba que la posición exista en los límites del tablero, que la celda no haya sido marcada con bandera"
            "y que no haya minas en ninguna de sus posiciones vecinas, es decir, que el valor de la celda sea cero como se quiere."
            "Por otra parte, se excluye a aquellos elementos ya registrados previamente, pues el resultado final no contendrá repetidos:"

            if es_pos_valida(tablero, new_cord_fila, new_cord_columna) and tablero[new_cord_fila][new_cord_columna] == 0 and tablero_visible[new_cord_fila][new_cord_columna] != BANDERA and (new_cord_fila, new_cord_columna) not in res:
                res.append((new_cord_fila, new_cord_columna))

            "De llegar a una posición donde ninguno de sus vecinos cumpla con estas condiciones simultáneamente, nada se agregaría a res"
            "por lo que el bucle terminaría su ejecución (el índice supera la longitud de la lista res), terminando con la búsqueda de ceros."

        i_res += 1

    return res


def guardar_pos_adyacentes(fila: int, columna: int, tablero: list[list[int]])-> list[tuple[int, int]]: 

    "Recibe como parámetros in un número de fila, un número de columna y un tablero de juego, y devuelve una"
    "lista con todas las posiciones adyacentes a las coordenadas fila-columna indicadas. Por 'adyacentes' se"
    "entiende a las tres celdas inmediatamente superiores, las tres inferiores, la izquierda y la derecha;"
    "habiendo a lo sumo ocho posiciones de interés a devolver."

    res: list[tuple[int, int]] = []

    for i_fila in range(fila-1, fila+2):  # i_fila = fila-1, fila, fila+1
        for i_col in range(columna-1, columna+2):  # i_col = columna-1, columna, columna+1

            "Recorriendo el rango especificado anteriormente, decide si la posición es válida (existe"
            "en el tablero) y distinta de la posición de entrada, pues sólo interesan sus vecinas."

            if es_pos_valida(tablero, i_fila, i_col) and (i_fila, i_col) != (fila, columna):
                res.append((i_fila, i_col))

    return res


# Ejercicio 7.

def verificar_victoria(estado: EstadoJuego) -> bool:
    return todas_celdas_seguras_descubiertas(estado['tablero'], estado["tablero_visible"])


# Ejercicio 8.

def reiniciar_juego(estado: EstadoJuego) -> None:
    filas: int = estado["filas"]
    columnas: int = estado["columnas"]
    minas: int = estado["minas"]
    
    nuevo_estado = crear_juego(filas, columnas, minas)
    for key in nuevo_estado.keys():
        estado[key] = nuevo_estado[key]


# Ejercicio 9.

def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


# Ejercicio 10.

def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
