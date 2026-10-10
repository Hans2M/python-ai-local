# Consultar API JSON con urllib

**Tema:** HTTP, APIs REST, peticiones y respuestas JSON  
**Nivel:** intermedio

Crear solicitud HTTP con timeout, capturar URLError y leer JSON. Requiere acceso al servidor indicado; el bot no realizará llamadas externas por sí mismo.

## Ejemplo en Python

```python
import json
import urllib.error
import urllib.request
url = "http://127.0.0.1:8000/estado"
try:
    with urllib.request.urlopen(url, timeout=3) as respuesta:
        datos = json.load(respuesta)
        print(datos)
except urllib.error.URLError as exc:
    print("Servicio no disponible:", exc)
```
