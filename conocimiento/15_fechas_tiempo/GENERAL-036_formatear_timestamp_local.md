# Formatear timestamp local

**Tema:** Fechas, horas y cálculo de intervalos  
**Nivel:** basico

Usar datetime.now y strftime para imprimir una marca de tiempo en el huso local del equipo.

## Ejemplo en Python

```python
from datetime import datetime
ahora = datetime.now().astimezone()
print(ahora.strftime("%Y-%m-%d %H:%M:%S %z"))
```
