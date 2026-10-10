# Reporte corto de switch

Pedir hostname, IP y cantidad de puertos, y mostrar reporte legible.

```python
nombre = input("Nombre: ").strip().upper()
ip = input("IP: ").strip()
puertos = int(input("Puertos: "))
print("--- INVENTARIO ---")
print(f"Nombre: {nombre}")
print(f"IP: {ip}")
print(f"Puertos: {puertos}")
```
