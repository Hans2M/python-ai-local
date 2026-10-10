# División segura

**Tema:** Errores, excepciones, try/except/finally y validación  
**Nivel:** basico

Capturar ValueError y ZeroDivisionError separadamente e informar el motivo.

## Ejemplo en Python

```python
try:
    a = float(input("Numerador: "))
    b = float(input("Denominador: "))
    print(a / b)
except ValueError:
    print("Entrada inválida")
except ZeroDivisionError:
    print("No se puede dividir entre cero")
```
