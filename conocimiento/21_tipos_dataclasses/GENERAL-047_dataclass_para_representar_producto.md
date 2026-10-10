# Dataclass para representar producto

**Tema:** Type hints, dataclasses y modelado de datos  
**Nivel:** intermedio

Usar @dataclass y anotaciones para generar inicializador y representar datos simples.

## Ejemplo en Python

```python
from dataclasses import dataclass

@dataclass
class Producto:
    nombre: str
    precio: float
    cantidad: int

    def subtotal(self) -> float:
        return self.precio * self.cantidad

producto = Producto("Lápiz", 1.5, 4)
print(producto.subtotal())
```
