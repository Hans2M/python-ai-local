# Validar rango y tipo

**Tema:** Validación, secretos, rutas seguras y calidad del código  
**Nivel:** basico

Separar conversión y validación, produciendo mensajes claros por entradas no válidas.

## Ejemplo en Python

```python
def edad_valida(texto):
    try:
        edad = int(texto)
    except ValueError:
        return False
    return 0 <= edad <= 120

print(edad_valida("25"))
print(edad_valida("abc"))
```
