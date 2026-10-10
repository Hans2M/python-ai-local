# Guardar y leer JSON

**Tema:** Serialización JSON y archivos CSV  
**Nivel:** intermedio

Serializar un diccionario con json.dumps; recuperar con json.loads y mantener caracteres Unicode.

## Ejemplo en Python

```python
import json
from pathlib import Path
persona = {"nombre": "María", "edad": 22}
ruta = Path("persona.json")
ruta.write_text(json.dumps(persona, ensure_ascii=False, indent=2), encoding="utf-8")
datos = json.loads(ruta.read_text(encoding="utf-8"))
print(datos["nombre"])
```
