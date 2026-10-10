# Usar módulos de la biblioteca estándar

**Tema:** Módulos, importaciones, paquetes y entornos virtuales  
**Nivel:** basico

Importar math para calcular la raíz cuadrada y evitar nombres locales que oculten módulos.

## Ejemplo en Python

```python
import math
numero = float(input("Número no negativo: "))
if numero >= 0:
    print(math.sqrt(numero))
else:
    print("Entrada negativa")
```
