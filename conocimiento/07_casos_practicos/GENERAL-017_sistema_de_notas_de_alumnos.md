# Sistema de notas de alumnos

**Tema:** Ejercicios integradores y problemas aplicados  
**Nivel:** basico

Representar alumnos con diccionarios, calcular promedios y clasificar aprobados.

## Ejemplo en Python

```python
alumnos = {"Ana": [14, 16, 13], "Luis": [9, 12, 10]}
for nombre, notas in alumnos.items():
    promedio = sum(notas) / len(notas)
    estado = "Aprobado" if promedio >= 11 else "Desaprobado"
    print(f"{nombre}: {promedio:.1f} - {estado}")
```
