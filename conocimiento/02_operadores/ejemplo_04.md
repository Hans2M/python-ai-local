# Capacidad de enlaces

Multiplicar cantidad de puertos por velocidad de cada puerto para estimar su capacidad total en Mbps.

```python
puertos = int(input("Puertos: "))
velocidad = int(input("Mbps por puerto: "))
capacidad = puertos * velocidad
print(f"Capacidad teórica: {capacidad} Mbps")
```
