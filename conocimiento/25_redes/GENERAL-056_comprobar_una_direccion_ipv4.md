# Comprobar una dirección IPv4

**Tema:** IPv4, sockets básicos y automatización de redes local  
**Nivel:** basico

Validar una dirección IPv4 con ipaddress, sin conectarse a la red.

## Ejemplo en Python

```python
from ipaddress import IPv4Address

def ipv4_valida(texto):
    try:
        IPv4Address(texto)
        return True
    except ValueError:
        return False

print(ipv4_valida("192.168.1.10"))
print(ipv4_valida("999.1.2.3"))
```
