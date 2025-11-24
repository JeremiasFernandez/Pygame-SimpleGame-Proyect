@echo off
REM ============================================================================
REM Bossfight: El Troyano - Launcher Universal
REM ============================================================================
REM Este script ejecuta el juego desde cualquier ubicacion del sistema
REM No importa donde este instalado el proyecto
REM ============================================================================

echo.
echo ========================================
echo   Bossfight: El Troyano
echo   Iniciando juego...
echo ========================================
echo.

REM Obtener la ubicacion de este script
set "SCRIPT_DIR=%~dp0"

REM Navegar a la carpeta Juego/Codigo (relativa a este script)
cd /d "%SCRIPT_DIR%Juego\Codigo"

REM Verificar que Python esta disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Python no esta instalado o no esta en el PATH
    echo.
    echo Opciones:
    echo   1. Instala Python desde https://www.python.org/
    echo   2. O usa el ejecutable: Bossfight_ElTroyano.exe
    echo.
    pause
    exit /b 1
)

REM Verificar que las dependencias estan instaladas
python -c "import pygame" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ADVERTENCIA] pygame no esta instalado
    echo.
    echo Instalando dependencias automaticamente...
    echo.
    
    REM Volver a la raiz para usar requirements.txt
    cd /d "%SCRIPT_DIR%"
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo.
        echo [ERROR] No se pudieron instalar las dependencias
        echo Por favor ejecuta manualmente: pip install pygame pillow
        echo.
        pause
        exit /b 1
    )
    
    REM Volver a Juego/Codigo
    cd /d "%SCRIPT_DIR%Juego\Codigo"
    echo.
    echo [OK] Dependencias instaladas correctamente
    echo.
)

REM Ejecutar el juego
echo Iniciando Bossfight: El Troyano...
echo.
python main.py

REM Si hubo error, pausar para ver el mensaje
if errorlevel 1 (
    echo.
    echo [ERROR] El juego se cerro con un error
    echo.
    pause
)
