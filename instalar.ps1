# Instalador local de PYTHON AI LOCAL - Windows 10/11, PowerShell 5.1+
# Requisitos: acceso a Internet SOLO durante la instalacion inicial.
param(
    [switch]$NoInstalarDependencias,
    [switch]$NoDescargarModelo,
    [switch]$SinInicioAutomatico
)
$ErrorActionPreference = 'Stop'
$raiz = (Resolve-Path $PSScriptRoot).Path
$env:OLLAMA_NO_CLOUD = '1'
$nombreModelo = 'qwen2.5:3b'
Write-Host '=== Instalacion de PYTHON AI LOCAL ==='
Write-Host "Carpeta: $raiz"

function Buscar-Python {
    $candidatos = @()
    foreach($comando in @('python.exe', 'python')) {
        $r = Get-Command $comando -ErrorAction SilentlyContinue
        if ($r -and $r.Source) { $candidatos += $r.Source }
    }
    $carpeta = Join-Path $env:LOCALAPPDATA 'Programs\Python'
    if(Test-Path $carpeta) {
        $candidatos += @(Get-ChildItem -Path $carpeta -Recurse -Filter 'python.exe' -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch '(?i)\\scripts\\|\\lib\\' } | Select-Object -ExpandProperty FullName)
    }
    foreach($p in ($candidatos | Select-Object -Unique)) {
        try {
            $res = & $p -c 'import sys; print("OK" if sys.version_info >= (3, 10) else "OLD")' 2>$null
            if ($LASTEXITCODE -eq 0 -and "$res".Trim() -eq 'OK') { return $p }
        } catch { }
    }
    return $null
}
function Buscar-Ollama {
    $cmd = Get-Command 'ollama.exe' -ErrorAction SilentlyContinue
    if($cmd -and $cmd.Source) { return $cmd.Source }
    foreach($p in @((Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama.exe'), (Join-Path $env:ProgramFiles 'Ollama\ollama.exe'))) {
        if(Test-Path -LiteralPath $p) {return $p}
    }
    return $null
}
function Instalar-Winget([string]$id) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "No encuentro winget. Instala manualmente $id y repite la instalacion."
    }
    Write-Host "Instalando $id con winget (puede requerir confirmacion)..."
    & winget install -e --id $id --source winget --accept-source-agreements --accept-package-agreements
    if ($LASTEXITCODE -ne 0) { throw "winget no pudo instalar $id (codigo $LASTEXITCODE)" }
}
$python = Buscar-Python
if (-not $python -and -not $NoInstalarDependencias) {
    Instalar-Winget 'Python.Python.3.13'
    $python = Buscar-Python
}
if (-not $python) { throw 'Necesitas Python 3.10 o superior. Comprueba python --version.' }
Write-Host "Python: $python"

$ollama = Buscar-Ollama
if (-not $ollama -and -not $NoInstalarDependencias) {
    Instalar-Winget 'Ollama.Ollama'
    $ollama = Buscar-Ollama
}
if (-not $ollama) { throw 'Necesitas Ollama. Instalalo y vuelve a ejecutar este archivo.' }
Write-Host "Ollama: $ollama"

# Arrancar Ollama si no hay API accesible; si ya corre, no se abre otra instancia.
try {
    Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 | Out-Null
} catch {
    Write-Host 'Iniciando Ollama local...'
    Start-Process -FilePath $ollama -ArgumentList 'serve' -WindowStyle Hidden
    $listo = $false
    for($i=0;$i -lt 40;$i++) {
        Start-Sleep -Seconds 2
        try {
            Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 | Out-Null
            $listo = $true; break
        } catch { }
    }
    if(-not $listo) { throw 'Ollama no pudo iniciar su API en 127.0.0.1:11434' }
}
$modelos = & $ollama list 2>&1 | Out-String
if ($modelos -notmatch '(?m)^qwen2\.5:3b\s') {
    if ($NoDescargarModelo) {
        Write-Warning "No esta descargado el modelo $nombreModelo. Ejecuta: ollama pull $nombreModelo"
    } else {
        Write-Host "Descargando $nombreModelo (aproximadamente 2 GB). Internet necesario solo ahora."
        & $ollama pull $nombreModelo
        if ($LASTEXITCODE -ne 0) { throw 'No pudo descargarse el modelo Ollama.' }
    }
} else { Write-Host "Modelo disponible: $nombreModelo" }

# BATCH con ruta absoluta a Python. Solo modifica PATH del usuario.
$comando = Join-Path $raiz 'bot.cmd'
$texto = "@echo off`r`n" + '"' + $python + '" "%~dp0cliente.py" %*' + "`r`n"
[System.IO.File]::WriteAllText($comando, $texto, [System.Text.Encoding]::ASCII)
$rutaUsuario = [Environment]::GetEnvironmentVariable('Path','User')
$partes = @($rutaUsuario -split ';' | Where-Object {$_})
if (-not ($partes | Where-Object {$_.TrimEnd('\') -ieq $raiz.TrimEnd('\')})) {
    [Environment]::SetEnvironmentVariable('Path', (($partes + $raiz) -join ';'), 'User')
    Write-Host "Comando bot anadido al PATH de usuario: $raiz"
}
$env:Path += ";$raiz"

# Iniciar con Windows usando el mecanismo que se verifico en Windows real.
if (-not $SinInicioAutomatico) {
    $pythonw = Join-Path (Split-Path $python -Parent) 'pythonw.exe'
    if(-not (Test-Path $pythonw)) {$pythonw = $python}
    $inicio = [Environment]::GetFolderPath('Startup')
    New-Item -ItemType Directory -Force -Path $inicio | Out-Null
    $vbs = Join-Path $inicio 'PYTHON_AI_LOCAL_Arranque.vbs'
    $server = Join-Path $raiz 'servidor.py'
    $contenido = 'Set shell = CreateObject("WScript.Shell")' + "`r`n" + 'shell.Run """' + $pythonw + '"" ""' + $server + '""", 0, False' + "`r`n"
    [System.IO.File]::WriteAllText($vbs, $contenido, [System.Text.Encoding]::Unicode)
    Write-Host "Inicio automatico: $vbs"
    try {
        $tarea = Get-ScheduledTask -TaskName 'PYTHON_AI_LOCAL' -ErrorAction SilentlyContinue
        if ($tarea) { Disable-ScheduledTask -TaskName 'PYTHON_AI_LOCAL' -ErrorAction Stop | Out-Null }
    } catch { Write-Warning 'La tarea antigua no se pudo desactivar.' }
}

# Instala la extension local de VS Code; no es necesaria para usar bot desde terminal.
$vsix = Join-Path $raiz 'PYTHON_AI_LOCAL_Editor_Sincronizado.vsix'
if ((Test-Path $vsix) -and (Get-Command code -ErrorAction SilentlyContinue)) {
    try {
        & code --install-extension $vsix --force | Out-Host
        Write-Host 'Extension de VS Code instalada. Reinicia VS Code para activarla.'
    } catch { Write-Warning 'No se instalo la extension VS Code. El bot CLI sigue funcionando.' }
}

# Evitar duplicar servidor que ya esta activo.
$servidorActivo = $false
try {
    $r = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/estado' -TimeoutSec 2
    if($r.servidor -eq 'activo'){$servidorActivo = $true}
} catch { }
if (-not $servidorActivo) {
    $pythonw = Join-Path (Split-Path $python -Parent) 'pythonw.exe'
    if(-not (Test-Path $pythonw)){$pythonw=$python}
    Start-Process -FilePath $pythonw -ArgumentList ('"' + (Join-Path $raiz 'servidor.py') + '"') -WorkingDirectory $raiz -WindowStyle Hidden
    for($i=0;$i -lt 25;$i++) {
        Start-Sleep -Seconds 1
        try {
            $r=Invoke-RestMethod -Uri 'http://127.0.0.1:8765/estado' -TimeoutSec 2
            if($r.servidor -eq 'activo'){$servidorActivo=$true;break}
        } catch { }
    }
}
if($servidorActivo){Write-Host 'SERVIDOR ACTIVO.'}
else{Write-Warning 'Servidor aun no disponible. Revisa logs\servidor.log.'}
Write-Host ''
Write-Host 'INSTALACION TERMINADA. Abre una nueva terminal y usa: bot estado'
Write-Host 'Ejemplo: bot resolver ejercicio.txt --escribir --intervalo 5'
