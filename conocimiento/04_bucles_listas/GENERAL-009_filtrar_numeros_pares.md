# Filtrar números pares

**Tema:** Bucles for/while, listas, rangos y comprensiones  
**Nivel:** basico

Dada una lista de enteros, crear una segunda lista con los pares y sumar sus elementos.

## Ejemplo en Python

```python
numeros = [3, 8, 12, 5, 7, 10]
pares = [n for n in numeros if n % 2 == 0]
print("Pares:", pares)
print("Suma:", sum(pares))
```
