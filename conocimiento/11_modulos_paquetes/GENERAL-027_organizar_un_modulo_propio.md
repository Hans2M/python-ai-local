# Organizar un módulo propio

**Tema:** Módulos, importaciones, paquetes y entornos virtuales  
**Nivel:** intermedio

Separar funciones reutilizables en utilidades.py e importarlas desde principal.py. No llamar random.py ni json.py a scripts propios porque ocultan módulos estándar.

## Ejemplo en Python

```python
# Archivo utilidades.py
def duplicar(numero):
    return numero * 2

# Desde otro archivo: from utilidades import duplicar
```
