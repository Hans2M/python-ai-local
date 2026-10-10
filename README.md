# PYTHON AI LOCAL — Instalación desde GitHub

Asistente de ejercicios de Python, sin internet **después de la primera instalación**. Incluye el cliente actualizado para `resolver`, `revisar`, `corregir`, `reproducir`, `exportar`, escritura progresiva, pausa F6 y reanudación F7 (en VS Code con extensión instalada). Utiliza Ollama y el modelo **qwen2.5:3b** instalado en cada PC. **No se distribuyen los pesos del modelo.**

## Aviso antes de hacer público este repositorio

Esta edición pública incluye solamente **ejemplos originales** de los siete temas, sin reproducir las guías del docente ni el banco de soluciones que compartiste. Puedes conservar esos materiales en tu instalación personal, pero **no los subas a GitHub sin autorización**. **Para que otra persona instale desde un enlace sin autenticación, el repositorio debe ser público.**

## Cómo publicar (propietario)

1. Cambia `MasterGateway/python-ai-local` por tu usuario y repositorio reales en la variable `$Repositorio` de `instalar-online.ps1`.
2. Abre una terminal en la raíz, instala y autentica Git y GitHub CLI cuando sea necesario (`gh auth login`).
3. Ejecuta:

```powershell
git init
git branch -M main
git add .
git commit -m "Primera versión de Python AI Local"
gh repo create python-ai-local --public --source . --remote origin --push
```

Comando oficial `gh repo create`: https://cli.github.com/manual/gh_repo_create

## Cómo instalar (otros usuarios, Windows PowerShell)

### Recomendado: descargar el script, inspeccionarlo y ejecutarlo

```powershell
$url = 'https://raw.githubusercontent.com/MasterGateway/python-ai-local/main/instalar-online.ps1'
Invoke-WebRequest -Uri $url -OutFile "$env:TEMP\instalar-python-ai.ps1"
notepad "$env:TEMP\instalar-python-ai.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:TEMP\instalar-python-ai.ps1"
```

### Un solo comando (solo si confías en el autor y ya revisaste el script)

```powershell
irm https://raw.githubusercontent.com/MasterGateway/python-ai-local/main/instalar-online.ps1 | iex
```

**Importante:** sustituye `MasterGateway` por el propietario real de GitHub. Este comando descarga y ejecuta código remoto con tus permisos; úsalo solo en repositorios fiables. El instalador descarga el proyecto y, si faltan, intenta instalar Python 3.13 y Ollama mediante `winget`; descarga `qwen2.5:3b` (aprox. 2 GB) si falta. La primera instalación **necesita internet**, espacio libre y en algunos equipos intervención del usuario. Después funciona offline.

Por defecto instala en `%LOCALAPPDATA%\Programs\PythonAILocal` (ruta que **no debes mover**) y configura el inicio automático mediante la carpeta Inicio de Windows; no utiliza la antigua tarea programada. Instala la extensión VS Code si detecta el comando `code`.

## Uso (nueva terminal)

```powershell
bot estado
bot temas
bot resolver ejercicio.txt
bot resolver ejercicio.txt --escribir --intervalo 5
bot revisar main.py
bot corregir main.py
bot exportar .\soluciones\ejercicio_solucion.py
```

En VS Code: **F6 pausa** y **F7 reanuda** el modo progresivo si la extensión auxiliar está activa. Comentarios y líneas vacías no añaden el intervalo. También se puede `bot reproducir` desde un `.md` existente.

## Cómo actualizar

Vuelve a ejecutar `instalar-online.ps1`. Se mantiene `conocimiento/` si ya existe un índice local para no borrar los ejercicios añadidos por el usuario. El instalador hace una actualización in situ del código; **si el servidor ya está ejecutándose, reinicia Windows para cargar la versión nueva**.

## Carpetas locales que nunca debes subir

`.env`, `logs/`, `.bot_sesiones/`, `soluciones/`, `.venv/`, credenciales de Telegram/API, historiales de consultas, archivos personales y modelos `.gguf` / `.safetensors`. Consulta `.gitignore`.

## Seguridad

Todo escucha en `127.0.0.1`; el bot no ejecuta automáticamente el código sugerido, y la comprobación de sintaxis no garantiza la lógica. La instalación online requiere verificar el origen del código. No exposes el servidor por red pública sin autenticarlo.

## Diferencia entre edición pública y edición personal

La edición pública incorpora una base inicial de 14 fichas originales. La base personal del curso tiene 82 registros y no debe publicarse sin comprobar permisos de difusión.
