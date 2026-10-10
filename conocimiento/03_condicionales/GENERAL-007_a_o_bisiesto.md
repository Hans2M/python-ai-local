# Año bisiesto

**Tema:** Decisiones if, elif, else y validación de datos  
**Nivel:** basico

Un año es bisiesto si es divisible por 400 o si es divisible por 4 pero no por 100.

## Ejemplo en Python

```python
anio = int(input("Año: "))
es_bisiesto = anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)
print("Bisiesto" if es_bisiesto else "No bisiesto")
```
