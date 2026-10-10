# CSV con encabezados

**Tema:** Serialización JSON y archivos CSV  
**Nivel:** intermedio

Escribir y leer CSV usando csv.DictWriter y csv.DictReader, evitando separar manualmente por comas.

## Ejemplo en Python

```python
import csv
with open("alumnos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["nombre", "nota"])
    writer.writeheader()
    writer.writerow({"nombre": "Ana", "nota": 18})
with open("alumnos.csv", newline="", encoding="utf-8") as f:
    for fila in csv.DictReader(f):
        print(fila["nombre"], int(fila["nota"]))
```
