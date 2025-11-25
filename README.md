# Bossfight: El Troyano (Versión Código Fuente)

Un juego bullet-hell con elementos tipo RPG hecho en Python + Pygame.

## ✅ Objetivo de esta versión
Se eliminó toda distribución en ejecutable (.exe) y scripts de compilación para mantener el repositorio liviano y centrado en desarrollo.

## 🧪 Requisitos
- Python 3.10+ (recomendado)
- pip

## 📦 Dependencias
Declaradas en `requirements.txt`:
- pygame
- pillow (GIFs / imágenes)
- openai (opcional para diálogos IA)

## 🐍 Crear entorno virtual
### Windows
```bat
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python Juego\Codigo\main.py
```
### Linux / Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python Juego/Codigo/main.py
```
O usar los scripts automatizados:
```bat
setup_env.bat
```
```bash
bash setup_env.sh
```

## 🚀 Ejecutar el juego
Asegúrate de tener el entorno virtual activado:
```bash
python Juego/Codigo/main.py
```

## 📁 Estructura
```
Pygame-SimpleGame-Proyect/
  ├── setup_env.bat
  ├── setup_env.sh
  ├── requirements.txt
  ├── README.md
  └── Juego/
      ├── assets/        # Sprites, sonidos, música
      └── Codigo/        # Código fuente principal
          ├── main.py
          ├── Const.py
          ├── characters/
          └── screens/
```

## 💬 Diálogos con IA (Opcional)
Exporta tu API Key antes de ejecutar si deseas diálogos dinámicos:
```powershell
$env:OPENAI_API_KEY="tu_api_key"
```
Si no se establece, el juego usa diálogos predefinidos.

## 🔧 Desarrollo
Sugerencias:
- Activa modo fullscreen desde menú Opciones.
- Usa F1/F2 para debug / cheats.
- Estructura lista para añadir nuevos ataques y fases.

## 🧹 Limpieza realizada
- Eliminada carpeta `compilador/` y archivos .spec.
- Eliminado ejecutable grande (.exe) para evitar límite de 100 MB GitHub.
- README simplificado para desarrollo.

## 🐛 Reportar issues
Crear issue: https://github.com/JeremiasFernandez/Pygame-SimpleGame-Proyect/issues

## 📜 Licencia
MIT (añade archivo LICENSE si aún no existe).
