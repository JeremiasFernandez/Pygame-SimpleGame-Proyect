@echo off
REM =============================================================
REM Crear y activar entorno virtual para Bossfight: El Troyano
REM Uso: doble clic o ejecutar desde CMD
REM =============================================================

set VENV_DIR=.venv

if exist %VENV_DIR% (
  echo [INFO] Entorno virtual ya existe: %VENV_DIR%
) else (
  echo [INFO] Creando entorno virtual...
  python -m venv %VENV_DIR%
  if errorlevel 1 (
    echo [ERROR] Fallo creando entorno virtual.
    pause
    exit /b 1
  )
)

echo [INFO] Activando entorno...
call %VENV_DIR%\Scripts\activate.bat
if errorlevel 1 (
  echo [ERROR] No se pudo activar el entorno.
  pause
  exit /b 1
)

echo [INFO] Actualizando pip...
python -m pip install --upgrade pip >nul 2>&1

echo [INFO] Instalando dependencias del juego...
pip install -r ..\requirements.txt
if errorlevel 1 (
  echo [ERROR] Fallo instalando dependencias.
  pause
  exit /b 1
)

echo.
echo =============================================================
echo Entorno listo. Para ejecutar el juego:
echo    call %VENV_DIR%\Scripts\activate.bat
echo    cd ..
echo    python Juego\Codigo\main.py
echo =============================================================

echo Ejecutar ahora? (S/N)
set /p RUNNOW=
if /I "%RUNNOW%"=="S" (
  cd ..
  python Juego\Codigo\main.py
)

pause
