# Servidor HTTP mínimo

**Tema:** HTTP, APIs REST, peticiones y respuestas JSON  
**Nivel:** intermedio

Crear un servidor HTTP de prueba local ligado a 127.0.0.1; solo sirve archivos de la carpeta actual y debe usarse con precaución.

## Ejemplo en Python

```python
from http.server import HTTPServer, SimpleHTTPRequestHandler
if __name__ == "__main__":
    servidor = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
    print("Servidor local iniciado; Ctrl+C detiene")
    servidor.serve_forever()
```
