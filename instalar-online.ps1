# Instalador remoto de Python AI Local para Windows (PowerShell).
$ErrorActionPreference = 'Stop'
$Repositorio = 'MasterGateway/python-ai-local'
$Rama = 'main'
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
    # Guardar las entradas anteriores antes de copiar la biblioteca nueva.
    $kbActual = Join-Path $destino 'conocimiento\indice.jsonl'
    $entradasLocales = @()
    if (Test-Path -LiteralPath $kbActual) {
        $entradasLocales = @(Get-Content -LiteralPath $kbActual -Encoding UTF8 | Where-Object { $_.Trim() })
    }
    New-Item -ItemType Directory -Force -Path $destino | Out-Null
    Get-ChildItem -LiteralPath $carpeta.FullName -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $destino $_.Name) -Force -Recurse
    }
    # Fusionar por ID: preferir la versión nueva de los ejemplos incluidos,
    # conservar los ejercicios agregados por el usuario y los ID desconocidos.
    $kbNuevo = Join-Path $destino 'conocimiento\indice.jsonl'
    $ids = @{}
    foreach ($linea in @(Get-Content -LiteralPath $kbNuevo -Encoding UTF8)) {
        if (-not $linea.Trim()) { continue }
        try {
            $obj = $linea | ConvertFrom-Json
            if ($obj.id) { $ids[[string]$obj.id] = $true }
        } catch { }
    }
    $extra = New-Object 'System.Collections.Generic.List[string]'
    foreach ($linea in $entradasLocales) {
        try {
            $obj = $linea | ConvertFrom-Json
            if ($obj.id -and -not $ids.ContainsKey([string]$obj.id)) {
                $extra.Add($linea)
                $ids[[string]$obj.id] = $true
            }
        } catch {
            Write-Warning 'Se encontró una línea de conocimiento personalizada no válida; no se importó.'
        }
    }
    if ($extra.Count -gt 0) {
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::AppendAllText($kbNuevo, ($extra -join "`n") + "`n", $utf8)
        Write-Host "Referencias personales conservadas: $($extra.Count)"
    }
    Write-Host "Actualizado en: $destino"
    & (Join-Path $destino 'instalar.ps1')
} finally {
    Remove-Item -LiteralPath $tmp -Force -Recurse -ErrorAction SilentlyContinue
}
