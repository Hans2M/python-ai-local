# Argumentos por defecto

**Tema:** Funciones, argumentos, retorno, alcance y recursión  
**Nivel:** basico

Ilustrar un parámetro opcional en una función, y evitar listas mutables como valores por defecto.

## Ejemplo en Python

```python
def saludo(nombre, titulo=""):
    encabezado = f"{titulo} " if titulo else ""
    return f"Hola, {encabezado}{nombre}"

print(saludo("Ana"))
print(saludo("Luis", "Dr."))
```
