# Descomponer segundos

**Tema:** Operadores aritméticos, lógicos y comparaciones  
**Nivel:** basico

Convertir segundos en horas, minutos y segundos restantes usando // y %. Evitar asumir que el operador / produce enteros.

## Ejemplo en Python

```python
total = int(input("Segundos: "))
horas = total // 3600
minutos = (total % 3600) // 60
segundos = total % 60
print(f"{horas:02d}:{minutos:02d}:{segundos:02d}")
```
