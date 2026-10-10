# Listar archivos .py de una carpeta

**Tema:** Scripts de tareas, rutas, organización de archivos  
**Nivel:** basico

Recorrer una carpeta con pathlib y mostrar nombres de archivos Python sin modificar el sistema de archivos.

## Ejemplo en Python

```python
from pathlib import Path
carpeta = Path.cwd()
for archivo in sorted(carpeta.glob("*.py")):
    print(archivo.name)
```
