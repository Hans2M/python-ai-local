# Número primo

**Tema:** Búsqueda, ordenamiento, complejidad y algoritmos  
**Nivel:** basico

Determinar si n es primo comprobando divisores solo hasta su raíz cuadrada entera.

## Ejemplo en Python

```python
from math import isqrt

def es_primo(n):
    if n < 2:
        return False
    for divisor in range(2, isqrt(n) + 1):
        if n % divisor == 0:
            return False
    return True

print(es_primo(29))
```
