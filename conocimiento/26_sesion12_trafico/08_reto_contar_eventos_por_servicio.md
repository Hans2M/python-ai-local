# Reto: contar eventos por servicio

**Tema:** Sesión 12 — Análisis de registros de tráfico con Python  
**Nivel:** basico

Extender el análisis de la clase agregando un tercer Counter de servicios y acumulando servicios[fila["servicio"]] += 1 por cada evento. Mostrar la frecuencia por servicio. No sustituir los otros contadores obligatorios si el enunciado pide conservarlos.

## Ejemplo en Python

```python
import csv
from collections import Counter

servicios = Counter()
with open("trafico.csv", "r", newline="", encoding="utf-8-sig") as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        servicios[fila["servicio"]] += 1

print("Eventos por servicio:")
for servicio, cantidad in servicios.items():
    print(servicio, cantidad)
```
