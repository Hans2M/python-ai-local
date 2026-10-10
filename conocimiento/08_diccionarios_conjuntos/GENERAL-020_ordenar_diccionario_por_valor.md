# Ordenar diccionario por valor

**Tema:** Diccionarios, tuplas, conjuntos y colecciones  
**Nivel:** intermedio

Ordenar nombres por calificación mediante sorted con una clave.

## Ejemplo en Python

```python
notas = {"Ana": 18, "Luis": 14, "Marta": 16}
ordenados = sorted(notas.items(), key=lambda item: item[1], reverse=True)
for nombre, nota in ordenados:
    print(nombre, nota)
```
