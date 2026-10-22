# Ejercicio: agrupar eventos por origen y servicio

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Practicar dos contadores independientes: uno para origen y otro para servicio. No confundir esta agrupación con conexiones únicas.

## Ejemplo en Python

```python
import csv
from collections import Counter

por_origen = Counter()
por_servicio = Counter()
with open("trafico.csv", "r", newline="", encoding="utf-8-sig") as archivo:
    for fila in csv.DictReader(archivo):
        por_origen[fila["origen"]] += 1
        por_servicio[fila["servicio"]] += 1
print("Origen:", por_origen)
print("Servicio:", por_servicio)
```
