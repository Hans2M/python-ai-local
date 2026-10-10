# Validación de VLAN

Leer una VLAN, rechazar valores fuera del intervalo 1 a 4094 y reconocer la VLAN de laboratorio 250.

```python
vlan = int(input("VLAN: "))
if vlan < 1 or vlan > 4094:
    print("VLAN inválida")
elif vlan == 250:
    print("VLAN del laboratorio")
else:
    print("VLAN válida")
```
