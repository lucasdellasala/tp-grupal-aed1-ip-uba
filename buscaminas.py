import random
from typing import Any
import os

# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

BOMBA_CODIGO = -1
BANDERA_CODIGO = -2
VACIO_CODIGO = 0

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]


def existe_archivo(ruta_directorio: str, nombre_archivo: str) -> bool:
    """Chequea si existe el archivo en la ruta dada"""
    return os.path.exists(os.path.join(ruta_directorio, nombre_archivo))


def colocar_minas(filas: int, columnas: int, minas: int) -> list[list[int]]:
    contador_minas: int = 0
    posiciones_minas: list[int] = random.sample(
        range(1, filas * columnas), minas)
    tablero: list[list[int]] = []

    for fila in range(filas):
        tablero.append([])
        for columna in range(columnas):
            tablero[fila].append(VACIO_CODIGO)

    while contador_minas < minas:
        indice_mina = posiciones_minas[contador_minas]
        fila = indice_mina // columnas
        columna = indice_mina % columnas
        tablero[fila][columna] = BOMBA_CODIGO
        contador_minas += 1

    return tablero


def actualizar_contador(contador: int, indice_celda: int, fila: list[int], es_fila_actual: bool) -> int:
    contador_actualizado: int = contador

    if indice_celda-1 >= 0 and fila[indice_celda-1] == BOMBA_CODIGO:
        contador_actualizado += 1
    if fila[indice_celda] == BOMBA_CODIGO and not es_fila_actual:
        contador_actualizado += 1
    if indice_celda+1 < len(fila) and fila[indice_celda+1] == BOMBA_CODIGO:
        contador_actualizado += 1

    return contador_actualizado


def calcular_numeros(tablero: list[list[int]]) -> None:
    for indice_fila in range(len(tablero)):
        for indice_celda in range(len(tablero[indice_fila])):
            if tablero[indice_fila][indice_celda] == BOMBA_CODIGO:
                continue

            contador_minas_limitrofes: int = 0
            fila_superior: list[int] = []
            if indice_fila-1 >= 0:
                fila_superior = tablero[indice_fila-1]
            fila_actual: list[int] = tablero[indice_fila]
            fila_inferior: list[int] = []
            if indice_fila+1 < len(tablero):
                fila_inferior = tablero[indice_fila+1]

            if len(fila_superior) > 0:
                contador_minas_limitrofes = actualizar_contador(
                    contador_minas_limitrofes, indice_celda, fila_superior, False)
            if len(fila_actual) > 0:
                contador_minas_limitrofes = actualizar_contador(
                    contador_minas_limitrofes, indice_celda, fila_actual, True)
            if len(fila_inferior) > 0:
                contador_minas_limitrofes = actualizar_contador(
                    contador_minas_limitrofes, indice_celda, fila_inferior, False)

            tablero[indice_fila][indice_celda] = contador_minas_limitrofes


def crear_juego(filas: int, columnas: int, minas: int) -> EstadoJuego:
    return {}


def obtener_estado_tablero_visible(estado: EstadoJuego) -> list[list[str]]:
    return [[]]


def marcar_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def descubrir_celda(estado: EstadoJuego, fila: int, columna: int) -> None:
    return


def verificar_victoria(estado: EstadoJuego) -> bool:
    return True


def reiniciar_juego(estado: EstadoJuego) -> None:
    return


def guardar_estado(estado: EstadoJuego, ruta_directorio: str) -> None:
    return


def cargar_estado(estado: EstadoJuego, ruta_directorio: str) -> bool:
    return False
