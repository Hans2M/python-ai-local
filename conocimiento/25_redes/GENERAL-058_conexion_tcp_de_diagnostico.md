# Conexión TCP de diagnóstico

**Tema:** IPv4, sockets básicos y automatización de redes local  
**Nivel:** intermedio

Abrir socket TCP únicamente a localhost y comprobar si un puerto de prueba responde, usando timeout.

## Ejemplo en Python

```python
import socket
try:
    with socket.create_connection(("127.0.0.1", 8765), timeout=2):
        print("Puerto local disponible")
except OSError:
    print("Servicio local no disponible")
```
