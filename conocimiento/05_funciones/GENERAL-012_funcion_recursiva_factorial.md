# Función recursiva factorial

**Tema:** Funciones, argumentos, retorno, alcance y recursión  
**Nivel:** intermedio

Calcular n! con caso base y validación de enteros no negativos; explicar alternativa iterativa para n grande.

## Ejemplo en Python

```python
def factorial(n):
    if n < 0:
        raise ValueError("n debe ser no negativo")
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
```
