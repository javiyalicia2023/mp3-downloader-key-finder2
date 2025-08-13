# Instala Python, FFmpeg y dependencias, luego genera los ejecutables
# Uso: ejecutar este script con PowerShell en Windows

function Install-IfMissing {
    param(
        [string]$Command,
        [string]$PackageId,
        [string]$Display
    )
    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        Write-Host "Instalando $Display..."
        winget install -e --id $PackageId --silent
    } else {
        Write-Host "$Display ya está instalado."
    }
}

Install-IfMissing -Command "python" -PackageId "Python.Python.3.11" -Display "Python"
Install-IfMissing -Command "ffmpeg" -PackageId "Gyan.FFmpeg" -Display "FFmpeg"

Write-Host "Actualizando pip y paquetes..."
python -m ensurepip --upgrade | Out-Null
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Generando ejecutables..."
python build.py cli
python build.py gui

Write-Host "Todo listo. Los ejecutables se encuentran en la carpeta dist/"
