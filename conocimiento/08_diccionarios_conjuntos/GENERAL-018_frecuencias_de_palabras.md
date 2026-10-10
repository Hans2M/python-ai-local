# Frecuencias de palabras

**Tema:** Diccionarios, tuplas, conjuntos y colecciones  
**Nivel:** basico

Contar cuántas veces aparece cada palabra normalizada con un diccionario.

## Ejemplo en Python

```python
texto = "python permite aprender python"
frecuencias = {}
for palabra in texto.lower().split():
    frecuencias[palabra] = frecuencias.get(palabra, 0) + 1
print(frecuencias)
```
