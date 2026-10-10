# Python AI Local

**Asistente de programación Python que funciona en tu computadora con Ollama.** Permite resolver enunciados, revisar y corregir código, consultar ejemplos locales y guardar soluciones desde la terminal de Windows o VS Code.

La primera instalación necesita internet para obtener el programa, las dependencias y el modelo. **Después de instalar y descargar el modelo, el uso normal no necesita internet.** El servicio escucha solo en `127.0.0.1`.

## ¿Qué hace?

- **Resuelve** ejercicios de Python y produce una explicación `.md` y un programa `.py`.
- **Revisa** archivos Python sin ejecutar el código.
- **Corrige** programas y conserva el archivo original.
- **Escribe progresivamente** líneas de código con un intervalo configurable; los comentarios y las líneas vacías no agregan demora.
- **Pausa y reanuda** la escritura desde VS Code con `F6` y `F7`, si está instalada la extensión auxiliar.
- **Exporta** un `.py` a otra carpeta y puede abrir esa carpeta en una ventana nueva de VS Code.
- **Consulta y amplía** una biblioteca de ejemplos locales de Python.

El modelo predeterminado es **`qwen2.5:3b`**. El programa no distribuye los pesos del modelo y no garantiza que todas las respuestas sean correctas: revisa y prueba el código generado antes de usarlo.

## Requisitos

- Windows 10/11 con PowerShell.
- Python 3.10 o superior.
- Ollama y el modelo local `qwen2.5:3b`.
- VS Code es opcional, pero recomendable para la escritura progresiva y los controles de teclado.

El instalador intenta obtener Python, Ollama y el modelo si aún no están presentes. Se necesita conexión a internet durante esta preparación y espacio suficiente para los archivos del modelo.

## Instalación

**Opción recomendada:** descarga e inspecciona el instalador antes de ejecutarlo:

```powershell
$url = 'https://raw.githubusercontent.com/MasterGateway/python-ai-local/main/instalar-online.ps1'
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\instalar-python-ai.ps1"
notepad "$env:TEMP\instalar-python-ai.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\instalar-python-ai.ps1"
```

**Instalación rápida**, solo si confías en el repositorio y has revisado el script:

```powershell
irm https://raw.githubusercontent.com/MasterGateway/python-ai-local/main/instalar-online.ps1 | iex
```

Al finalizar, abre una terminal nueva y comprueba:

```powershell
bot estado
bot temas
```

La instalación se realiza, de manera predeterminada, en `%LOCALAPPDATA%\Programs\PythonAILocal`. El instalador configura el comando `bot` y el arranque del servidor local al iniciar sesión en Windows. **No necesitas instalar Git ni GitHub CLI para usar el bot.**

## Comandos

Desde cualquier carpeta de trabajo:

| Comando | Función |
| --- | --- |
| `bot estado` | Comprueba el servidor y Ollama. |
| `bot temas` | Muestra los temas disponibles en la biblioteca. |
| `bot resolver ejercicio.txt` | Resuelve el enunciado y guarda los resultados. |
| `bot revisar main.py` | Genera un informe de revisión, sin ejecutar el programa. |
| `bot corregir main.py` | Genera una propuesta de código corregido. |
| `bot buscar "sqlite y consultas"` | Busca referencias en la biblioteca local. |
| `bot resolver ejercicio.txt --tema poo` | Da preferencia a un tema concreto. |
| `bot resolver ejercicio.txt --escribir --intervalo 10` | Escribe progresivamente el código. |
| `bot reproducir .\soluciones\ejercicio_solucion.md --escribir --intervalo 5` | Reproduce una solución existente sin consultar el modelo otra vez. |
| `bot exportar .\soluciones\ejercicio_solucion.py` | Copia el `.py` a la carpeta elegida. |
| `bot agregar ejemplo.md --tema algoritmos` | Añade una referencia propia al índice local. |

### Ejemplo de ejercicio

Crea un archivo `ejercicio.txt` con:

```text
Tema: diccionarios

Solicita cinco nombres y sus edades. Guarda los datos en un diccionario
 y muestra el nombre de la persona de mayor edad.
```

Resuélvelo con:

```powershell
bot resolver ejercicio.txt
```

Los resultados se guardan en `soluciones/` dentro de la carpeta desde la que llamaste al bot:

```text
mi-proyecto/
├── ejercicio.txt
└── soluciones/
    ├── ejercicio_solucion.md
    └── ejercicio_solucion.py
```

Para ejecutar el `.py` generado **después de revisarlo**:

```powershell
python .\soluciones\ejercicio_solucion.py
```

### Escritura progresiva

```powershell
bot resolver ejercicio.txt --escribir --intervalo 60
```

El intervalo se aplica entre líneas ejecutables. Las líneas vacías y los comentarios aislados no agregan intervalos. En VS Code, `F6` pausa y `F7` reanuda cuando la extensión auxiliar está activa. También puedes pulsar `P` y `R` en la terminal del proceso.

**Importante:** mientras el archivo está controlado por el bot, las modificaciones manuales en el archivo generado pueden perderse. Conserva tus cambios en otro archivo.

### Exportar solo el código

```powershell
bot resolver ejercicio.txt --exportar --destino "C:\MisProgramas"
```

Se exporta solo el `.py`; la explicación permanece en la carpeta original. El archivo exportado obtiene un nombre alternativo si ya existe otro con el mismo nombre.

## Biblioteca general de Python

Incluye fundamentos, estructuras de control, funciones, archivos, diccionarios, expresiones regulares, excepciones, módulos, programación orientada a objetos, algoritmos, JSON, CSV, fechas, SQLite, APIs, pruebas, automatización, concurrencia, tipos, seguridad y redes, entre otros temas.

Consulta el índice:

```powershell
bot temas
bot buscar "consultas SQLite parametrizadas" --tema bases_datos
```

Para agregar referencias personalizadas puedes preparar un `.txt`, `.md` o `.py` y ejecutar:

```powershell
bot agregar mi_ejemplo.md --tema funciones
```

La biblioteca usa archivos JSONL para recuperar ejemplos relacionados; **no es entrenamiento de los pesos del modelo**. El modelo puede resolver también ejercicios sin ejemplos específicos, con resultados variables según el enunciado y la capacidad del modelo.

## Actualización

Vuelve a ejecutar el instalador de GitHub para actualizar los scripts y la biblioteca. El instalador combina las entradas nuevas con las referencias locales existentes para conservar los ejemplos personalizados.

Para que el proceso de servidor use el motor nuevo, reinicia Windows después de actualizar o reinicia el servidor local manualmente. Los comandos del cliente estarán disponibles en terminales nuevas.

## Solución de problemas

**`bot` no se reconoce:** abre una terminal nueva o reinicia VS Code para actualizar `PATH`.

**Error de conexión con el servidor:** ejecuta `bot estado`, comprueba Ollama y revisa `logs\servidor.log` en la carpeta de instalación.

**Falta el modelo:** ejecuta `ollama list`. La descarga inicial se realiza con `ollama pull qwen2.5:3b` (con internet).

**Los atajos no responden:** confirma que la extensión auxiliar esté instalada y que estés usando el editor de VS Code.

**La respuesta contiene errores:** especifica las restricciones del ejercicio, usa `bot revisar` y comprueba manualmente el código. La validación sintáctica no demuestra que un programa funcione correctamente.

## Privacidad y seguridad

- El servidor del asistente se limita a `127.0.0.1`; no se publica automáticamente en internet.
- Ollama se consulta mediante su API local.
- El código generado no se ejecuta automáticamente.
- No añadas contraseñas, tokens, archivos `.env` ni información privada al repositorio.
- Las llamadas HTTP que un programa generado pueda incluir son independientes del funcionamiento local del bot; revísalas antes de ejecutarlas.

Esta herramienta ofrece ayuda para aprender y programar; no sustituye la revisión humana ni las pruebas.
