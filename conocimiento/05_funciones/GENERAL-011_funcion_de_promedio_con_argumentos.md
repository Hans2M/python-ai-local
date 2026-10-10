# Función de promedio con argumentos

**Tema:** Funciones, argumentos, retorno, alcance y recursión  
**Nivel:** basico

Una función recibe una colección numérica y devuelve su promedio; manejar correctamente una lista vacía.

## Ejemplo en Python

```python
def promedio(numeros):
    if not numeros:
        raise ValueError("La lista no puede estar vacía")
    return sum(numeros) / len(numeros)

print(promedio([12, 15, 18]))
```
