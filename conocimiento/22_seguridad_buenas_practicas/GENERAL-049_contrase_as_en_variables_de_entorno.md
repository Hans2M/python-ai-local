# Contraseñas en variables de entorno

**Tema:** Validación, secretos, rutas seguras y calidad del código  
**Nivel:** basico

Leer configuración con os.environ sin incrustar secretos en código ni imprimirlos.

## Ejemplo en Python

```python
import os
clave = os.environ.get("MI_APP_TOKEN")
if clave is None:
    print("Configura MI_APP_TOKEN")
else:
    print("Configuración disponible")
```
