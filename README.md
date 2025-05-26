# Buscaminas: TP Grupal AED1 / IP FCEN UBA

Este repositorio contiene el Trabajo Práctico grupal de la materia AED1 / IP de la Facultad de Ciencias Exactas y Naturales UBA.

## Descripción del proyecto

El proyecto consiste en un buscaminas implementado en Python de acuerdo a los requerimientos del documento [enunciado.pdf](enunciado.pdf).

## Objetivo del proyecto

Aprender las bases de la programación imperativa.

## Contribuidores

- Axel Alem
- Lucas Della Sala
- Marco García

> [!NOTE]  
> Al ser una actividad académica no está permitido la contribución de terceros.

## Metodología de contribución

Las contribuciones se realizaron de manera individual, pero con la posibilidad de discutir ideas a través de Pull Requests de un branch con nombre {feat|fix|chore}/{nombre_funcionalidad}.

- `feat`: Se agrega una nueva funcionalidad.
- `fix`: Se corrige un bug.
- `chore`: Se realiza un cambio no funcional, como refactorizar código.

> [!WARNING]  
> Un PR no puede contener múltiples funcionalidades.

### Configuración inicial

Después de clonar el repositorio, debes instalar los hooks de Git que validan el formato de commits y branches:

En Windows (PowerShell):
```powershell
.\.githooks\install.ps1
```

En Linux/Mac:
```bash
chmod +x .githooks/install.sh
./.githooks/install.sh
```

### Formato de contribuciones

#### Nombre de branch
```
{feat|fix|chore}/{nombre_funcionalidad}
Ejemplo: feat/colocar_minas
```

#### Título de PR
```
{feat|fix|chore}: descripción
Ejemplo: feat: Colocar minas
```

#### Descripción de PR
```
Se agrega la funcionalidad de colocar minas en el tablero.
```

### Aprobación de código

Los Pull Requests deben ser aprobados por los dos integrantes del grupo que no son autores de la funcionalidad.
