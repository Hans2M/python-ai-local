# Crear respaldos sin sobrescribir

**Tema:** Scripts de tareas, rutas, organización de archivos  
**Nivel:** intermedio

Copiar un archivo a una carpeta de respaldos con marca de tiempo; comprobar que el origen existe.

## Ejemplo en Python

```python
from datetime import datetime
from pathlib import Path
from shutil import copy2
origen = Path("documento.txt")
if origen.is_file():
    respaldo = Path("respaldos")
    respaldo.mkdir(exist_ok=True)
    destino = respaldo / f"{origen.stem}_{datetime.now():%Y%m%d_%H%M%S}{origen.suffix}"
    copy2(origen, destino)
    print(destino)
else:
    print("No existe el archivo original")
```
