@echo off
echo ============================================
echo   Moviendo ejecutable a carpeta principal
echo ============================================
echo.

if exist "dist\Bossfight_ElTroyano.exe" (
    echo Copiando ejecutable...
    copy /Y "dist\Bossfight_ElTroyano.exe" "..\..\Bossfight_ElTroyano.exe"
    echo.
    echo [OK] Ejecutable movido exitosamente!
    echo Ubicacion: Pygame-SimpleGame-Proyect\Bossfight_ElTroyano.exe
    echo.
    echo Puedes ejecutar el juego desde la carpeta principal ahora.
) else (
    echo [ERROR] No se encontro el ejecutable en dist\
    echo Asegurate de haber compilado primero ejecutando desde Juego/compilador
)

echo.
pause
