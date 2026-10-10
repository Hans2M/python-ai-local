# Entrada y salida con tipos

**Tema:** Sintaxis, variables, tipos de datos, entrada y salida  
**Nivel:** basico

Solicitar nombre y edad, convertir entrada a entero e imprimir texto formateado. input siempre devuelve str; int puede fallar si el usuario no escribe número.

## Ejemplo en Python

```python
nombre = input("Nombre: ").strip()
edad = int(input("Edad: "))
print(f"Hola, {nombre}. Tienes {edad} años.")
```
