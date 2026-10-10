# CLI con argparse

**Tema:** Argumentos CLI, argparse, organización de proyectos  
**Nivel:** intermedio

Crear comando que acepta el nombre de usuario mediante argumento opcional; mostrar ayuda con --help.

## Ejemplo en Python

```python
import argparse
parser = argparse.ArgumentParser(description="Saludar desde la terminal")
parser.add_argument("--nombre", default="mundo")
args = parser.parse_args()
print(f"Hola, {args.nombre}")
```
