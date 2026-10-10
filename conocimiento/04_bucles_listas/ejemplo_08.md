# Conteo de interfaces caídas

Recorrer una lista de estados y contar los que sean down.

```python
estados = ["up", "down", "up", "down"]
caidas = 0
for estado in estados:
    if estado == "down":
        caidas += 1
print("Interfaces caídas:", caidas)
```
