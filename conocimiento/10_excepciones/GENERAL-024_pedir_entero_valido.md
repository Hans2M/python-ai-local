# Pedir entero válido

**Tema:** Errores, excepciones, try/except/finally y validación  
**Nivel:** basico

Repetir la entrada hasta obtener un número entero válido; capturar ValueError, no ocultar todo error.

## Ejemplo en Python

```python
while True:
    try:
        edad = int(input("Edad: "))
        break
    except ValueError:
        print("Escribe un número entero")
print("Edad:", edad)
```
