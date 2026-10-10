# Inventario simple de productos

**Tema:** Ejercicios integradores y problemas aplicados  
**Nivel:** intermedio

Crear un inventario en memoria con diccionarios, listar productos y calcular el valor total.

## Ejemplo en Python

```python
productos = [
    {"nombre": "Cuaderno", "precio": 8.5, "cantidad": 4},
    {"nombre": "Lápiz", "precio": 1.2, "cantidad": 10},
]
total = 0
for producto in productos:
    subtotal = producto["precio"] * producto["cantidad"]
    total += subtotal
    print(producto["nombre"], subtotal)
print("Valor total:", round(total, 2))
```
