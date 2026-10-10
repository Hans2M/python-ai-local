# Normalizar texto para comparar

**Tema:** Cadenas, procesamiento de texto y expresiones regulares  
**Nivel:** basico

Quitar espacios exteriores y comparar sin distinguir mayúsculas y minúsculas.

## Ejemplo en Python

```python
usuario = input("Usuario: ").strip().casefold()
if usuario == "administrador":
    print("Nombre reconocido")
else:
    print("Otro usuario")
```
