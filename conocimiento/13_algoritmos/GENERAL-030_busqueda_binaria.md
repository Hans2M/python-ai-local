# Búsqueda binaria

**Tema:** Búsqueda, ordenamiento, complejidad y algoritmos  
**Nivel:** intermedio

Buscar un objetivo en una lista previamente ordenada y devolver posición o -1. Complejidad O(log n).

## Ejemplo en Python

```python
def busqueda_binaria(numeros, objetivo):
    izquierda, derecha = 0, len(numeros) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if numeros[medio] == objetivo:
            return medio
        if numeros[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

print(busqueda_binaria([1, 3, 5, 7, 9], 7))
```
