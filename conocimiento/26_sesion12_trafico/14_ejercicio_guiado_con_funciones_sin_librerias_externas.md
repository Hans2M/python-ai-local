# Ejercicio guiado con funciones sin librerias externas

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** intermedio

Si el enunciado pide funciones, encapsular la lectura y los conteos sin modificar el archivo fuente ni usar bibliotecas externas. Es una extensión didáctica respecto al script de clase.

## Ejemplo en Python

```python
import csv
from collections import Counter

def analizar_trafico(ruta):
    eventos = 0
    bytes_totales = 0
    acciones = Counter()
    origenes = Counter()
    with open(ruta, "r", newline="", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            eventos += 1
            bytes_totales += int(fila["bytes"])
            acciones[fila["accion"]] += 1
            origenes[fila["origen"]] += 1
    return eventos, bytes_totales, acciones, origenes

print(analizar_trafico("trafico.csv"))
```
