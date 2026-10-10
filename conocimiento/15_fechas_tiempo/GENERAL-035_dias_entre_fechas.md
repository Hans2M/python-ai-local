# Días entre fechas

**Tema:** Fechas, horas y cálculo de intervalos  
**Nivel:** basico

Convertir cadenas ISO AAAA-MM-DD a date y restar para obtener días.

## Ejemplo en Python

```python
from datetime import date
inicio = date.fromisoformat("2026-10-01")
fin = date.fromisoformat("2026-10-10")
print("Días:", (fin - inicio).days)
```
