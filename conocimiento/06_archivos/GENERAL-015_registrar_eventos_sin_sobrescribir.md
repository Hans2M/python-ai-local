# Registrar eventos sin sobrescribir

**Tema:** Lectura, escritura y manejo de archivos de texto  
**Nivel:** basico

Agregar un texto a un archivo usando modo a con with open, manteniendo los registros anteriores.

## Ejemplo en Python

```python
mensaje = input("Evento: ")
with open("eventos.txt", "a", encoding="utf-8") as archivo:
    archivo.write(mensaje.strip() + "\n")
print("Evento registrado")
```
