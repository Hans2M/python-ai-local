# Booleanos y comparación de tipos

**Tema:** Sintaxis, variables, tipos de datos, entrada y salida  
**Nivel:** basico

Diferenciar str, int, float, bool y None; comprobar tipos con type y distinguir entre la cadena "False" y el booleano False.

## Ejemplo en Python

```python
activo = True
valor = "False"
print(type(activo).__name__)
print(type(valor).__name__)
print(activo == bool(valor))
```
