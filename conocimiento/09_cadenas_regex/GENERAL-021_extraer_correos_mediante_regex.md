# Extraer correos mediante regex

**Tema:** Cadenas, procesamiento de texto y expresiones regulares  
**Nivel:** basico

Usar re.findall para localizar correos con un patrón simple; no sustituye una validación completa de correo.

## Ejemplo en Python

```python
import re
texto = "Contactos: ana@example.com y luis@test.org"
correos = re.findall(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", texto)
print(correos)
```
