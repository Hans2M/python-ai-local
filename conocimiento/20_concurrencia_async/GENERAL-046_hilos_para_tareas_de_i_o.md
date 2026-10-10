# Hilos para tareas de I/O

**Tema:** Hilos, asyncio, concurrencia y operaciones I/O  
**Nivel:** intermedio

Lanzar varios hilos con ThreadPoolExecutor para tareas que esperan I/O, no para acelerar cálculos CPU intensivos.

## Ejemplo en Python

```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def trabajo(n):
    sleep(0.1)
    return n * 2

with ThreadPoolExecutor(max_workers=3) as pool:
    print(list(pool.map(trabajo, [1, 2, 3])))
```
