# Agrupar registros en SQL

**Tema:** SQLite, consultas SQL parametrizadas y persistencia  
**Nivel:** intermedio

Usar COUNT, GROUP BY y ORDER BY para obtener frecuencias por categoría en SQLite.

## Ejemplo en Python

```python
import sqlite3
with sqlite3.connect(":memory:") as con:
    con.execute("CREATE TABLE ventas (categoria TEXT)")
    con.executemany("INSERT INTO ventas VALUES (?)", [("libros",), ("libros",), ("ropa",)])
    for categoria, cantidad in con.execute("SELECT categoria, COUNT(*) FROM ventas GROUP BY categoria ORDER BY cantidad DESC"):
        print(categoria, cantidad)
```
