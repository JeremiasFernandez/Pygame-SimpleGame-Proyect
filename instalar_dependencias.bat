@echo off
REM ============================================================================
REM Bossfight: El Troyano - Script de Instalacion Automatica
REM ============================================================================
REM Este script instala automaticamente todas las dependencias necesarias
REM para ejecutar el juego desde codigo fuente.
REM ============================================================================

echo.
echo ========================================
echo   Bossfight: El Troyano
echo   Instalacion de Dependencias
echo ========================================
echo.

REM Verificar que Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar que pip esta disponible
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip no esta disponible
    echo Intenta: python -m ensurepip --upgrade
    pause
    exit /b 1
)

echo [OK] pip detectado
pip --version
echo.

REM Instalar dependencias desde requirements.txt
echo ========================================
echo Instalando dependencias...
echo ========================================
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Hubo un problema instalando las dependencias
    echo.
    echo Intenta instalar manualmente:
    echo   pip install pygame pillow openai
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo [EXITO] Instalacion completada!
echo ========================================
echo.
echo Ahora puedes jugar ejecutando:
echo   cd Juego\Codigo
echo   python main.py
echo.
echo O simplemente haz doble clic en "Bossfight_ElTroyano.exe"
echo.
pause
