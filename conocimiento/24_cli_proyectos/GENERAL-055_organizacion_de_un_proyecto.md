# Organización de un proyecto

**Tema:** Argumentos CLI, argparse, organización de proyectos  
**Nivel:** basico

Separar funciones y entrada principal usando if __name__ == "__main__", evitando efectos al importar.

## Ejemplo en Python

```python
def saludar(nombre):
    return f"Hola, {nombre}"

def main():
    print(saludar("Python"))

if __name__ == "__main__":
    main()
```
