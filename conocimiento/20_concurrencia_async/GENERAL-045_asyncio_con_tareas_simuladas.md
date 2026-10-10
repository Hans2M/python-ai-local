# asyncio con tareas simuladas

**Tema:** Hilos, asyncio, concurrencia y operaciones I/O  
**Nivel:** intermedio

Aprender await y gather con tareas locales de espera; no requiere conexión a internet.

## Ejemplo en Python

```python
import asyncio

async def tarea(nombre, segundos):
    await asyncio.sleep(segundos)
    return f"{nombre}: lista"

async def main():
    respuestas = await asyncio.gather(tarea("A", 0.1), tarea("B", 0.2))
    print(respuestas)

asyncio.run(main())
```
