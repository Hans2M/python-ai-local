# Pruebas unitarias con unittest

**Tema:** Pruebas unitarias, depuración y pruebas de casos límite  
**Nivel:** intermedio

Probar valores normales y casos límite de una función, sin necesidad de internet.

## Ejemplo en Python

```python
import unittest

def suma(a, b):
    return a + b

class PruebaSuma(unittest.TestCase):
    def test_enteros(self):
        self.assertEqual(suma(2, 3), 5)

    def test_negativos(self):
        self.assertEqual(suma(-1, 1), 0)

if __name__ == "__main__":
    unittest.main()
```
