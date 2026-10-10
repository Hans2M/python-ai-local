# Contar palabras sin puntuación

**Tema:** Cadenas, procesamiento de texto y expresiones regulares  
**Nivel:** basico

Usar expresiones regulares para extraer palabras de una cadena, contando por separado las letras acentuadas.

## Ejemplo en Python

```python
import re
texto = "Hola, mundo. ¡Hola Python!"
palabras = re.findall(r"\b\w+\b", texto.lower())
print("Cantidad:", len(palabras))
print(palabras)
```
