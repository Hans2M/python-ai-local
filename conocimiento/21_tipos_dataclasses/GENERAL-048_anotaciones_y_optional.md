# Anotaciones y Optional

**Tema:** Type hints, dataclasses y modelado de datos  
**Nivel:** intermedio

Usar anotaciones para documentar tipos sin suponer que Python las valida automáticamente.

## Ejemplo en Python

```python
def buscar_nota(notas: dict[str, float], nombre: str) -> float | None:
    return notas.get(nombre)

print(buscar_nota({"Ana": 17.0}, "Ana"))
```
