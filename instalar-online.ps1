# ESTE SCRIPT SE PUBLICA EN GitHub (carpeta raiz del repositorio).
# ANTES DE SUBIR: cambia la variable $Repositorio por MasterGateway/python-ai-local.
# En un repositorio PUBLICO, cualquier usuario puede descargarlo sin credenciales.
$ErrorActionPreference = 'Stop'
$Repositorio = 'MasterGateway/python-ai-local'  # CAMBIAR una sola vez antes de publicar
$Rama = 'main'
if($Repositorio.StartsWith('MasterGateway/')) {
    throw 'El propietario debe cambiar MasterGateway por su nombre real de GitHub en instalar-online.ps1.'
}
$destino = Join-Path $env:LOCALAPPDATA 'Programs\PythonAILocal'
$zipUrl = "https://github.com/$Repositorio/archive/refs/heads/$Rama.zip"
$tmp = Join-Path $env:TEMP ('PythonAILocal-' + [guid]::NewGuid().ToString('N'))
$zip = Join-Path $tmp 'proyecto.zip'
try {
    New-Item -ItemType Directory -Force -Path $tmp | Out-Null
    Write-Host "Descargando $Repositorio desde GitHub..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $zipUrl -OutFile $zip -UseBasicParsing
    Expand-Archive -Path $zip -DestinationPath (Join-Path $tmp 'extraido') -Force
    $carpeta = Get-ChildItem -Path (Join-Path $tmp 'extraido') -Directory | Select-Object -First 1
    if(-not $carpeta -or -not (Test-Path (Join-Path $carpeta.FullName 'servidor.py'))) {
        throw 'El repositorio no tiene servidor.py en la raiz. Comprueba la estructura publicada.'
    }
    $kbActual = Join-Path $destino 'conocimiento\indice.jsonl'
    $preservarKB = Test-Path $kbActual
    New-Item -ItemType Directory -Force -Path $destino | Out-Null
    # Mantener KB personalizada en actualizaciones.
    Get-ChildItem -LiteralPath $carpeta.FullName -Force | ForEach-Object {
        if ($preservarKB -and $_.Name -eq 'conocimiento') {return}
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $destino $_.Name) -Force -Recurse
    }
    Write-Host "Descargado en: $destino"
    & (Join-Path $destino 'instalar.ps1')
} finally {
    Remove-Item -LiteralPath $tmp -Force -Recurse -ErrorAction SilentlyContinue
}
