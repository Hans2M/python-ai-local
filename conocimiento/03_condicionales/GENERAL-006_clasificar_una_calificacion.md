# Clasificar una calificación

**Tema:** Decisiones if, elif, else y validación de datos  
**Nivel:** basico

Solicitar una nota entre 0 y 20; primero validar rango, luego imprimir aprobado desde 11 y desaprobado debajo.

## Ejemplo en Python

```python
nota = float(input("Nota: "))
if nota < 0 or nota > 20:
    print("Nota fuera del rango")
elif nota >= 11:
    print("Aprobado")
else:
    print("Desaprobado")
```
