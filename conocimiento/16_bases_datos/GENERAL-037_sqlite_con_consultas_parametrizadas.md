# SQLite con consultas parametrizadas

**Tema:** SQLite, consultas SQL parametrizadas y persistencia  
**Nivel:** intermedio

Crear tabla, insertar y consultar registros usando sqlite3 y placeholders ? para evitar inyección SQL.

## Ejemplo en Python

```python
import sqlite3
with sqlite3.connect("alumnos.db") as con:
    con.execute("CREATE TABLE IF NOT EXISTS alumnos (id INTEGER PRIMARY KEY, nombre TEXT)")
    con.execute("INSERT INTO alumnos(nombre) VALUES (?)", ("Ana",))
    for fila in con.execute("SELECT id, nombre FROM alumnos WHERE nombre = ?", ("Ana",)):
        print(fila)
```
