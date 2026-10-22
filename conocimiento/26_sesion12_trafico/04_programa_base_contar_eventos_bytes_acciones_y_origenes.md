# Programa base: contar eventos, bytes, acciones y origenes

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Reproducir la lógica esencial de sesion12_analizar_trafico.py: abrir trafico.csv, recorrer sus filas con DictReader, sumar int(bytes), contar acciones y origenes con Counter, e imprimir cuatro resultados. Conservar el archivo csv en la misma carpeta desde la que se ejecuta Python.

## Ejemplo en Python

```python
import csv
from collections import Counter

acciones = Counter()
origenes = Counter()
total_eventos = 0
total_bytes = 0

with open("trafico.csv", "r", newline="", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        total_eventos += 1
        total_bytes += int(fila["bytes"])
        acciones[fila["accion"]] += 1
        origenes[fila["origen"]] += 1

print("Eventos:", total_eventos)
print("Bytes:", total_bytes)
print("Por accion:", acciones)
print("Por origen:", origenes)
```
