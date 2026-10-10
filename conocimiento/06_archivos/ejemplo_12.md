# Registro de asistencia

Guardar una línea nombre,estado en asistencia.txt sin borrar registros anteriores.

```python
nombre = input("Nombre: ").strip()
estado = input("Estado (presente/ausente): ").strip().lower()
with open("asistencia.txt", "a", encoding="utf-8") as archivo:
    archivo.write(f"{nombre},{estado}\n")
print("Registro guardado")
```
