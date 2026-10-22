# Sesión 12 — Análisis de registros de tráfico con Python

Esta ampliación del conocimiento de **Python AI Local** se basa en la sesión 12 del material de Programabilidad de Redes compartido por el usuario. La biblioteca es una **adaptación didáctica original**, no una copia pública de la guía universitaria.

## Objetivo de la sesión

Leer un CSV de eventos de red, contar filas, sumar los bytes y agrupar eventos por acción y origen usando exclusivamente bibliotecas estándar de Python.

**Columnas del archivo:** `fecha`, `hora`, `origen`, `destino`, `servicio`, `accion`, `bytes`.

**Métodos vistos:** `import csv`, `from collections import Counter`, `csv.DictReader`, `int()`, `for`, `with open(..., newline="", encoding="utf-8-sig")`, `print()`.

## Ejecución del material de ejemplo

Abre PowerShell en la carpeta `ejemplos/sesion12_trafico` y ejecuta:

```powershell
python analizar_trafico.py
python analizar_trafico_por_servicio.py
```

El CSV incluido tiene **8 registros ficticios creados para esta actualización**. No es el CSV del profesor. Los resultados indicados en la guía original (99 eventos y 142690 bytes) únicamente corresponden al conjunto de datos del docente.

## Usar el bot con el tema nuevo

Desde cualquier carpeta de ejercicios, con un archivo `ejercicio.txt`:

```powershell
bot resolver ejercicio.txt --tema sesion12
bot resolver ejercicio.txt --tema sesion12 --escribir --intervalo 10
bot revisar analizar_trafico.py --tema sesion12
bot corregir analizar_trafico.py --tema sesion12
bot temas
```

También reconoce si el enunciado empieza con `Tema: sesion12` o si menciona `trafico.csv`, «sesión 12» o «registros de tráfico».

La selección de tema y los ejemplos mejoran la contextualización, pero **no garantizan** que un modelo pequeño acierte todos los casos. Revisa y ejecuta el código con el CSV real que te den.

## Retos de la guía

1. Agregar un evento `PERMITIR` de 300 bytes y comparar resultados.
2. Agrupar también por `servicio`.
3. Distinguir el número de eventos del número de personas o conexiones únicas.
4. Reconocer que registros ficticios no prueban tráfico de una red real.

