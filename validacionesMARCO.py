from typing import Any
from buscaminas import calcular_numeros, copiar_matriz
# Constantes para dibujar
BOMBA = chr(128163)  # simbolo de una mina
BANDERA = chr(127987)  # simbolo de bandera blanca
VACIO = " "  # simbolo vacio inicial

# Tipo de alias para el estado del juego
EstadoJuego = dict[str, Any]

def es_matriz(matriz:list[list[Any]])-> bool:
    res:bool = True
    for filas in matriz:
        res = res and len(filas) == len(matriz[0])
    return res
    

def cantidad_de_minas(tablero: list[list[int]])-> int:
    res: int = 0
    for fila in tablero:
        for casilla in fila:
            if casilla == -1:
                res += 1 
    return res


def todas_las_celdas_descubiertas(tablero:list[list[int]], tablero_visible:list[list[str]]):
    # ve si todas las celdas seguras fueron descubiertas sin tomar en cuenta las minas 
    for i_filas in range(len(tablero)):
        for i_columnas in range(len(tablero[0])):
            celda = tablero[i_filas][i_columnas]
            celda_visible = tablero_visible[i_filas][i_columnas]
            # si la celda no es una mina y ya fue descubierta
            if celda != -1 and celda_visible == VACIO: 
                return False
    return True

def descubrio_una_bomba(tablero_visible:list[list[str]])-> bool:
    # Veo si en tablero_visible hay una bomba 
    for i_fila in range(len(tablero_visible)):
        for i_columna in range(len(tablero_visible[0])):
            if tablero_visible[i_fila][i_columna] == BOMBA:
                return True
    return False

def son_matriz_y_misma_dimension(tablero: list[list[int]], tablero_visible: list[list[int]])->bool:
    # Verifica si son matrices válidas
    if not (es_matriz(tablero) and es_matriz(tablero_visible)):
        return False
    # verifica que tienen el mismo número de filas
    if len(tablero) != len(tablero_visible): 
        return False
    # Verfica que cada fila tiene el mimo número de filas
    res:bool = True 
    for i in range(len(tablero)):
        res = res and len(tablero[i]) == len(tablero_visible[i])
    return res

def estado_valido(estado:EstadoJuego)->bool:
    filas = estado['filas']
    columnas = estado['columnas']
    minas = estado['minas']
    tablero = estado['tablero']
    tablero_visible = estado['tablero_visible']
    juego_terminado = estado['juego_terminado']
    
    # La cantidad de minas del tablero es igual a las minas del estado
    if cantidad_de_minas(tablero) != minas:
        return False # preguntar a Valen si puedo hacer esto. 
    
    # Verifica si el tablero tiene los numeros correctos
    tablero_aux = copiar_matriz(tablero)
    calcular_numeros(tablero_aux)
    if tablero_aux != tablero:
        return False
    
    
    # Veo si el juego debió haber terminado con el estado del tablero y tablero_visible
    terminó_el_juego = todas_las_celdas_descubiertas(tablero, tablero_visible) or descubrio_una_bomba(tablero_visible)
    if juego_terminado and not (terminó_el_juego):
        return False
    if not (juego_terminado) and terminó_el_juego:
        return False
    
    # Las coordenadas de las bombas visibles corresponde con bombas reales (las del tablero)
    for i_fila in range(filas):
        for i_columna in range(columnas):
            if tablero_visible[i_fila][i_columna] == BOMBA and tablero[i_fila][i_columna] != -1:
                return False
    
    # tablero implica tablero visible.
    for i_fila in range(filas):
        for i_columna in range(columnas):
            casilla_tablero_visible =tablero_visible[i_fila][i_columna]
            casilla_tablero = tablero[i_fila][i_columna]
            if tablero_visible[i_fila][i_columna] not in [BOMBA,BANDERA, VACIO ]:
                if casilla_tablero_visible != str(casilla_tablero):
                    return False
    return True

def tipos_validos(valores:list[Any], tipo:Any):
    # Verifica que todos los valores sean del mismo tipo
    res: bool = True
    for valor in valores:
        res = res and type(valor) == type(tipo)
    return res

def estan_desde(valores:list[Any], desde:Any):
    # Verifica que todos los valores sean mayores desde
    res: bool = True
    for valor in valores:
        res = res and desde < valor 
    return res

def estan_hasta(valores:list[Any], hasta:Any):
    # Verifica que todos los valores sean menores hasta
    res: bool = True
    for valor in valores:
        res = res and  valor < hasta 
    return res

def estan_en_rango(valores:list[Any], desde:Any, hasta:Any):
    # Verifica usando desde y hasta que los valores están en rango
    return estan_desde(valores, desde) and estan_hasta(valores, hasta)

def valores_pertenecen(valores:list[Any], pertenece:list[Any]):
    # Verifica que todos los valores estén en pertenece
    res: bool = True
    for valor in valores:
         res = res and valor in pertenece
    return res

def convertir_en_lista(matriz:list[list[Any]])-> list[Any]:
    # Convierte a una matriz a una lista
    res:list[Any] = []
    for fila in matriz:
        for casilla in fila:
            res.append(casilla)
    return res

def estructura_y_tipos_validos(estado:EstadoJuego)->bool:
    # Extracción de los valores de estado
    filas = estado['filas']
    columnas = estado['columnas']
    minas = estado['minas']
    juego_terminado = estado['juego_terminado']
    tablero = estado['tablero']
    tablero_visible = estado['tablero_visible']
    
    # Validación de tipos (no sé como mandar un tipo como parametro)
    if not (tipos_validos([filas, columnas, minas], 1)):
        return False
     
    if not(type(juego_terminado)== bool):
        return False
    
    # Validacion de rangos
    if not (estan_desde([filas, columnas], 0)):
        return False
    
    if not(estan_en_rango([minas], 0, filas * columnas)):
        return False
    
    if not(estan_en_rango(convertir_en_lista(tablero), -2, 9)): #estan_en_rango es mayor estricto
        return False
    
    
    # Pertenencia
    
    "Lista de valores permitidos en tablero_visible"
    valores_de_tablero_visible = [VACIO, BOMBA, BANDERA]
    for numero in range(9):
        valores_de_tablero_visible.append(str(numero))
    
    
    if not(valores_pertenecen(convertir_en_lista(tablero_visible), valores_de_tablero_visible)):
        return False
    
    # Validación de dimensiones y consistencia entre tableros
    if not (son_matriz_y_misma_dimension(tablero, tablero_visible) and
            len(tablero) == filas and
            len(tablero[0]) == columnas):
        return False
    return True
estado:EstadoJuego = {'filas': 10, 'columnas': 10, 'minas': 10, 'tablero_visible': [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']], 'juego_terminado': False, 'tablero': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 1, -1, 1, 0, 1, 1, 2, 1, 1], [0, 1, 1, 1, 0, 1, -1, 2, -1, 1], [0, 1, 1, 1, 0, 2, 2, 4, 2, 2], [0, 1, -1, 2, 1, 2, -1, 3, -1, 2], [0, 1, 1, 2, -1, 2, 1, 3, -1, 2], [0, 0, 0, 2, 2, 2, 1, 2, 2, 1], [0, 0, 0, 1, -1, 1, 1, -1, 1, 0], [0, 0, 0, 1, 1, 1, 1, 1, 1, 0]]}
print(estructura_y_tipos_validos(estado))