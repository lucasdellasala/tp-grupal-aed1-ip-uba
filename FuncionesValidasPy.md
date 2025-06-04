# Listado de funciones permitidas para el parcial de Python

Cualquier otra función debe ser implementada. Si utilizan una función no permitida, se anula el ejercicio.

---

## Conversión de tipos

- `int`, `list`, `float`, `str`, `tuple`, `bool`

## Estructuras

- `if-else-elif`
- `while`
- `for` (pueden usar `for in range(..)` o `for in secuencia`)

## Rango

- `range(i, f, p)` (pueden usar 3, 2 o 1 parámetro)

## Operadores aritméticos

- `+`, `-`, `*`, `/`, `//`, `sqrt`, `round`, `floor`, `ceil`, `%`

## Operadores lógicos

- `and`, `or`, `not`, `==`, `!=`, `>`, `<`, `>=`, `<=`

## Sobre secuencias

- Pertenece: `in`
- Concatenación: `+`
- Repetición: `*`
- Longitud: `len`
- Acceso a elementos: `s[elem]`  
  *(No está permitido usar `s[i:f]`, `s[-i]` o similar)*

## Listas

- `append(e)`
- `clear()`
- `pop()`
- `copy()`

## Diccionarios

- `items()`
- `keys()`
- `values()`
- `pop(clave)`
- `clear()`

## TAD Pilas

```python
from queue import LifoQueue
pila = LifoQueue()
pila.put(e)
pila.get()
pila.empty()
```

## TAD Colas

```python
from queue import Queue
cola = Queue()
cola.put(e)
cola.get()
cola.empty()
```

## Otros

* El uso de `break`/`continue` está permitido.

## Archivos

* `open`
* `read`
* `readline`
* `readlines`
* `write`
* `writelines`
* `close`
* `os.path.join()`
* `os.path.exists()`

---

> Recordar que todas las variables deben ir anotadas con su tipo correspondiente.
