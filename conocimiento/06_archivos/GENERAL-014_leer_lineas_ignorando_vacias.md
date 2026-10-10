# Leer líneas ignorando vacías

**Tema:** Lectura, escritura y manejo de archivos de texto  
**Nivel:** basico

Leer archivo UTF-8, limpiar espacios y omitir líneas vacías sin eliminar el archivo. El archivo de entrada debe existir.

## Ejemplo en Python

```python
from pathlib import Path
ruta = Path("datos.txt")
if ruta.is_file():
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            print(linea.strip())
else:
    print("No existe datos.txt")
```
