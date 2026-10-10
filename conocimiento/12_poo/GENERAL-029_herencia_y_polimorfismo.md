# Herencia y polimorfismo

**Tema:** Clases, objetos, herencia, métodos y encapsulación  
**Nivel:** intermedio

Usar una clase base y una derivada, sobrescribiendo un método.

## Ejemplo en Python

```python
class Animal:
    def hablar(self):
        return "Sonido"

class Perro(Animal):
    def hablar(self):
        return "Guau"

animales = [Animal(), Perro()]
for animal in animales:
    print(animal.hablar())
```
