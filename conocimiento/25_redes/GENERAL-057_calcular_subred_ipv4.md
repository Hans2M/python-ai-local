# Calcular subred IPv4

**Tema:** IPv4, sockets básicos y automatización de redes local  
**Nivel:** basico

Usar IPv4Network para consultar dirección de red, broadcast y prefijo CIDR sin llamadas de red.

## Ejemplo en Python

```python
from ipaddress import IPv4Network
red = IPv4Network("192.168.10.0/26")
print("Red:", red.network_address)
print("Broadcast:", red.broadcast_address)
print("Prefijo:", red.prefixlen)
print("Direcciones:", red.num_addresses)
```
