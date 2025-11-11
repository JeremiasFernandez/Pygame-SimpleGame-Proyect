# Carpeta de Compilación

Esta carpeta contiene todos los archivos necesarios para compilar el juego en un ejecutable .exe

## 📦 Archivos

- `bossfight.spec` - Configuración de PyInstaller
- `create_icon.py` - Genera el ícono del .exe
- `build_simple.ps1` - Script para compilar automáticamente
- `mover_exe.bat` - Mueve el .exe a la carpeta raíz
- `game_icon.ico` - Ícono del ejecutable

## 🔨 Cómo Compilar

### Método Simple:
```powershell
cd Juego/compilador
.\build_simple.ps1
```

### Método Manual:
```powershell
cd Juego/compilador
python create_icon.py
pyinstaller --clean --noconfirm bossfight.spec
mover_exe.bat
```

## 📁 Resultado

El ejecutable se generará en:
- `dist/Bossfight_ElTroyano.exe` (temporal)
- `../../Bossfight_ElTroyano.exe` (final)
