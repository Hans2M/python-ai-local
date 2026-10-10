# Depuración de entrada inválida

**Tema:** Pruebas unitarias, depuración y pruebas de casos límite  
**Nivel:** basico

Identificar diferencia entre errores de sintaxis, excepciones en ejecución y fallos lógicos; utilizar casos de prueba y logging en lugar de silenciar excepciones.

## Ejemplo en Python

```python
import logging
logging.basicConfig(level=logging.INFO)

def area(ancho, alto):
    if ancho < 0 or alto < 0:
        raise ValueError("Dimensiones negativas")
    logging.info("Calculando área")
    return ancho * alto

print(area(3, 4))
```
