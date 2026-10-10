# Ordenamiento de burbuja

**Tema:** Búsqueda, ordenamiento, complejidad y algoritmos  
**Nivel:** intermedio

Implementar bubble sort con bucles anidados para comprender intercambios; en producción sorted suele ser mejor.

## Ejemplo en Python

```python
def burbuja(lista):
    copia = lista.copy()
    for fin in range(len(copia) - 1, 0, -1):
        for i in range(fin):
            if copia[i] > copia[i + 1]:
                copia[i], copia[i + 1] = copia[i + 1], copia[i]
    return copia

print(burbuja([9, 2, 5, 1]))
```
