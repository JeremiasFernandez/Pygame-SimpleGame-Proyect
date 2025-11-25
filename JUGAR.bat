@echo off
REM Launcher simple sin .exe, usa entorno virtual si existe
set VENV_DIR=.venv

if exist %VENV_DIR% (
  call %VENV_DIR%\Scripts\activate.bat
  if errorlevel 1 (
    echo [WARNING] No se pudo activar .venv, continuando sin venv
  )
) else (
  echo [INFO] No existe .venv. Crealo con: setup_env.bat
)

echo Iniciando juego...
python Juego\Codigo\main.py
if errorlevel 1 (
  echo [ERROR] El juego finalizó con error.
  pause
)
