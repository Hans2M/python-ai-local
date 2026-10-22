# Ejercicio: reportar eventos bloqueados

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Contar cuántos eventos aparecen con accion BLOQUEAR, manteniendo el contador Counter del programa base. La consulta no demuestra qué conexiones se rechazaron realmente fuera del CSV de práctica.

## Ejemplo en Python

```python
import csv
from collections import Counter

acciones = Counter()
with open("trafico.csv", "r", newline="", encoding="utf-8-sig") as archivo:
    for fila in csv.DictReader(archivo):
        acciones[fila["accion"]] += 1
print("BLOQUEAR:", acciones["BLOQUEAR"])
```
