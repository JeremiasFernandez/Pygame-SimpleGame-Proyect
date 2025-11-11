# ============================================================================
# Script de Compilación para Bossfight: El Troyano
# ============================================================================
# Este script automatiza la creación del ejecutable .exe del juego
# Incluye todas las dependencias y assets necesarios
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Compilador de Bossfight: El Troyano  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: No se encuentra main.py" -ForegroundColor Red
    Write-Host "Por favor, ejecuta este script desde la carpeta Juego/Codigo" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "📦 Paso 1: Verificando dependencias..." -ForegroundColor Yellow

# Verificar si PyInstaller está instalado
$pyinstallerInstalled = python -m pip list | Select-String "pyinstaller"

if (-not $pyinstallerInstalled) {
    Write-Host "⚠️  PyInstaller no está instalado" -ForegroundColor Yellow
    Write-Host "Instalando PyInstaller..." -ForegroundColor Cyan
    python -m pip install pyinstaller
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar PyInstaller" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "✅ PyInstaller instalado correctamente" -ForegroundColor Green
} else {
    Write-Host "✅ PyInstaller ya está instalado" -ForegroundColor Green
}

# Verificar otras dependencias
Write-Host ""
Write-Host "📋 Verificando otras dependencias..." -ForegroundColor Yellow

$dependencies = @("pygame", "pillow", "openai")
$missingDeps = @()

foreach ($dep in $dependencies) {
    $installed = python -m pip list | Select-String $dep
    if (-not $installed) {
        $missingDeps += $dep
        Write-Host "⚠️  $dep no está instalado" -ForegroundColor Yellow
    } else {
        Write-Host "✅ $dep está instalado" -ForegroundColor Green
    }
}

if ($missingDeps.Count -gt 0) {
    Write-Host ""
    Write-Host "Instalando dependencias faltantes..." -ForegroundColor Cyan
    python -m pip install $missingDeps
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error al instalar dependencias" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "🎨 Paso 2: Generando ícono del juego..." -ForegroundColor Yellow

python create_icon.py

if (-not (Test-Path "game_icon.ico")) {
    Write-Host "⚠️  No se pudo crear el ícono, continuando sin ícono personalizado..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 Paso 3: Compilando ejecutable..." -ForegroundColor Yellow
Write-Host "Esto puede tomar varios minutos..." -ForegroundColor Cyan
Write-Host ""

# Limpiar builds anteriores
if (Test-Path "build") {
    Write-Host "🧹 Limpiando compilaciones anteriores..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Compilar con PyInstaller usando el archivo .spec
pyinstaller --clean --noconfirm bossfight.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Error durante la compilación" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "✅ Compilación completada exitosamente!" -ForegroundColor Green
Write-Host ""

# Verificar que se creó el ejecutable
if (Test-Path "dist\Bossfight_ElTroyano.exe") {
    $exeSize = (Get-Item "dist\Bossfight_ElTroyano.exe").Length / 1MB
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  🎮 EJECUTABLE CREADO EXITOSAMENTE!  " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Ubicación: dist\Bossfight_ElTroyano.exe" -ForegroundColor Cyan
    Write-Host "📊 Tamaño: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎯 El ejecutable incluye:" -ForegroundColor Yellow
    Write-Host "   ✓ Todas las bibliotecas de Python" -ForegroundColor White
    Write-Host "   ✓ Pygame y sus dependencias" -ForegroundColor White
    Write-Host "   ✓ Todos los assets (sonidos, sprites, música)" -ForegroundColor White
    Write-Host "   ✓ Integración con OpenAI (opcional)" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Para ejecutar el juego:" -ForegroundColor Yellow
    Write-Host "   Simplemente haz doble clic en: dist\Bossfight_ElTroyano.exe" -ForegroundColor White
    Write-Host ""
    
    # Preguntar si abrir la carpeta
    $response = Read-Host "¿Quieres abrir la carpeta 'dist' ahora? (S/N)"
    if ($response -match "^[SsYy]") {
        explorer "dist"
    }
    
} else {
    Write-Host "❌ No se encontró el ejecutable generado" -ForegroundColor Red
    Write-Host "Revisa los mensajes de error arriba" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💡 Notas:" -ForegroundColor Cyan
Write-Host "   • El ejecutable está en la carpeta 'dist'" -ForegroundColor White
Write-Host "   • Puedes distribuir solo el archivo .exe" -ForegroundColor White
Write-Host "   • No requiere Python instalado para ejecutarse" -ForegroundColor White
Write-Host "   • Los assets ya están incluidos dentro del .exe" -ForegroundColor White
Write-Host ""

pause
