# Agrupar ventas por categoría

**Tema:** Procesamiento de datos y estadística descriptiva  
**Nivel:** intermedio

Sumar importes por categoría con defaultdict para un reporte simple.

## Ejemplo en Python

```python
from collections import defaultdict
ventas = [("A", 12.5), ("B", 8.0), ("A", 7.5)]
totales = defaultdict(float)
for categoria, monto in ventas:
    totales[categoria] += monto
print(dict(totales))
```
