# Recorrer matriz

**Tema:** Bucles for/while, listas, rangos y comprensiones  
**Nivel:** basico

Dada una matriz como lista de listas, recorrer filas y columnas sin asumir tamaños fijos.

## Ejemplo en Python

```python
matriz = [[1, 2, 3], [4, 5, 6]]
for fila in matriz:
    for valor in fila:
        print(valor, end=" ")
    print()
```
