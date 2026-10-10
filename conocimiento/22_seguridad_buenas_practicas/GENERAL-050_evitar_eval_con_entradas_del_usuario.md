# Evitar eval con entradas del usuario

**Tema:** Validación, secretos, rutas seguras y calidad del código  
**Nivel:** basico

Nunca usar eval con texto arbitrario; emplear int, float, listas de opciones permitidas o parsers seguros.

## Ejemplo en Python

```python
operaciones = {"sumar": lambda a, b: a + b, "restar": lambda a, b: a - b}
op = input("sumar o restar: ").strip().lower()
if op in operaciones:
    print(operaciones[op](10, 3))
else:
    print("Operación no permitida")
```
