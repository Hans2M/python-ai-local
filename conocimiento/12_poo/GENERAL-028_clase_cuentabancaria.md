# Clase CuentaBancaria

**Tema:** Clases, objetos, herencia, métodos y encapsulación  
**Nivel:** intermedio

Crear una clase con atributos, constructor y métodos para depositar y consultar saldo; no permitir montos negativos.

## Ejemplo en Python

```python
class CuentaBancaria:
    def __init__(self, saldo=0):
        if saldo < 0:
            raise ValueError("Saldo inicial inválido")
        self.saldo = saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("Monto inválido")
        self.saldo += monto

cuenta = CuentaBancaria(100)
cuenta.depositar(25)
print(cuenta.saldo)
```
