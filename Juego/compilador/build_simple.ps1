# Script simple para compilar y mover el .exe a la raíz
# ======================================================
# EJECUTAR DESDE: Juego/compilador/

Write-Host "Compilando el juego..." -ForegroundColor Cyan

# Generar icono
python create_icon.py

# Compilar
pyinstaller --clean --noconfirm bossfight.spec

# Mover el .exe a la raíz del proyecto
if (Test-Path "dist\Bossfight_ElTroyano.exe") {
    Write-Host "Moviendo ejecutable a la carpeta raiz..." -ForegroundColor Yellow
    Copy-Item "dist\Bossfight_ElTroyano.exe" "..\..\Bossfight_ElTroyano.exe" -Force
    Write-Host "Listo! El ejecutable esta en la carpeta principal del proyecto" -ForegroundColor Green
    Write-Host "Ubicacion: Pygame-SimpleGame-Proyect\Bossfight_ElTroyano.exe" -ForegroundColor Cyan
} else {
    Write-Host "Error: No se encontro el ejecutable" -ForegroundColor Red
}
