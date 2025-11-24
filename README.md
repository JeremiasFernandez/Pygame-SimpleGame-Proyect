# 🎮 Bossfight: El Troyano

<div align="center">

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)
![Status](https://img.shields.io/badge/status-pre--alpha-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Un juego de acción bullet-hell con elementos RPG desarrollado en Python con Pygame**

[🎮 Jugar Ahora](#-cómo-jugar) • [Características](#-características) • [Instalación](#-instalación) • [Controles](#-controles) • [Código Secreto](#-código-secreto)

</div>

---

## 🚀 ¡JUEGA AHORA!

**¿Quieres jugar inmediatamente?**

👉 **Haz doble clic en `Bossfight_ElTroyano.exe`** 👈

El ejecutable está en la **carpeta raíz** del proyecto. No necesitas instalar nada.

---

## ⚡ Instalación Rápida de Dependencias

**¿Quieres ejecutar el código fuente pero tienes problemas con las bibliotecas?**

### Windows - Método Súper Fácil 🪟

1. Haz doble clic en **`instalar_dependencias.bat`** (está en la carpeta raíz)
2. ¡Espera a que termine!
3. Listo, ya puedes jugar

### Todas las Plataformas - Método Universal 🌍

```bash
pip install -r requirements.txt
```

Esto instalará automáticamente: `pygame`, `pillow`, y `openai`

---

## 📖 Descripción

**Bossfight: El Troyano** es un proyecto universitario desarrollado para la materia **Programación 1** de la **UTN FRA** (Universidad Tecnológica Nacional - Facultad Regional Avellaneda). El juego combina mecánicas de bullet-hell con una narrativa inspirada en Undertale, donde enfrentas a un virus informático ruso con inteligencia artificial.

### 🎯 Historia

Eres un programador que descubre un virus maligno infiltrado en tu computadora. Este no es un virus común: es un troyano ruso avanzado diseñado para robar información sensible. En una batalla épica dentro del ciberespacio, deberás esquivar patrones de ataque cada vez más complejos mientras el virus te provoca con comentarios sarcásticos generados por IA.

---

## ✨ Características

### 🎮 Modos de Juego

- **Modo Historia**: Enfrenta al virus en una batalla progresiva con 3 fases
- **Modo Práctica**: Practica cualquier fase del jefe sin restricciones
- **Dificultades**: Junior y Senior (desbloquea al completar Junior)

### 🤖 Integración con IA

- **Diálogos dinámicos** generados por OpenAI GPT-3.5
- El boss responde con personalidad única (sarcástico, amenazante y ruso)
- Sistema de fallback offline si no hay conexión

### 🎨 Sistema de Fases

1. **Fase 1**: Ataques básicos (lluvia, diagonales, laterales)
2. **Fase 2**: Introducción de lanzas giratorias
3. **Fase 3**: Combinaciones complejas y patrones circulares

### 🎵 Audio Dinámico

- Música adaptativa según el progreso del jugador
- Efectos de sonido para cada acción
- Transiciones épicas entre fases
- Pantalla de victoria con música triunfal

### 🎬 Características Especiales

- **Introducción top-down** estilo RPG clásico
- **Animación de transición** estilo Undertale al entrar en batalla
- **Sistema de partículas** en pantalla de victoria
- **Sprites animados** para personajes y enemigos
- **GIFs animados** como fondos

---

## 🚀 Instalación y Ejecución

### 🎯 Opción 1: Ejecutable Standalone (Recomendado)

**¡La forma más fácil de jugar!** Simplemente descarga y ejecuta.

#### Descargar y Jugar

**Método 1: Desde el repositorio**
1. Descarga o clona el repositorio completo
2. El ejecutable `Bossfight_ElTroyano.exe` está en la carpeta raíz
3. Haz doble clic en `Bossfight_ElTroyano.exe`
4. ¡A jugar! 🎮

**Método 2: Desde Releases**
1. Ve a [Releases](https://github.com/JeremiasFernandez/Pygame-SimpleGame-Proyect/releases)
2. Descarga `Bossfight_ElTroyano.exe` (última versión)
3. Haz doble clic en el archivo
4. ¡A jugar! 🎮

**Ventajas:**
- ✅ No requiere Python instalado
- ✅ Todas las bibliotecas incluidas
- ✅ Assets integrados en el ejecutable
- ✅ Listo para jugar instantáneamente
- ✅ Un solo archivo, fácil de distribuir

---

### 💻 Opción 2: Ejecutar desde Código Fuente

#### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/JeremiasFernandez/Pygame-SimpleGame-Proyect.git
cd Pygame-SimpleGame-Proyect
```

#### Paso 2: Instalar Dependencias

**Opción A: Instalación Automática (Recomendado)**

```bash
pip install -r requirements.txt
```

**Opción B: Instalación Manual**

```bash
# Dependencias básicas (obligatorias)
pip install pygame pillow

# Opcional: para diálogos con IA
pip install openai
```

> **💡 Tip**: Si tienes problemas con los directorios o imports, asegúrate de ejecutar el juego desde `Juego/Codigo/` con `python main.py`

#### Paso 3: Configurar API Key (Opcional)

Si deseas usar la integración con OpenAI para diálogos dinámicos:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="tu-api-key-aqui"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=tu-api-key-aqui
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

> **Nota**: Si no configuras la API key, el juego usará diálogos predefinidos automáticamente.

#### Paso 4: Ejecutar el Juego

```bash
cd Juego/Codigo
python main.py
```

---

### 🔨 Opción 3: Compilar tu Propio Ejecutable

¿Quieres crear tu propia versión del `.exe`?

#### Requisitos Adicionales

```bash
pip install pyinstaller
```

#### Compilación Automática

**Usando el script de PowerShell (Windows):**

```powershell
cd Juego/Codigo
.\build_exe.ps1
```

El script automáticamente:
1. ✅ Verifica e instala dependencias
2. ✅ Genera el ícono del juego
3. ✅ Compila el ejecutable con PyInstaller
4. ✅ Empaqueta todos los assets

**Compilación Manual:**

```bash
cd Juego/Codigo

# Crear el ícono
python create_icon.py

# Compilar con PyInstaller (método simplificado)
pyinstaller --clean --onefile --noconsole --icon=game_icon.ico --add-data "..\assets;assets" --name Bossfight_ElTroyano main.py

# Mover el ejecutable a la carpeta raíz
mover_exe.bat
```

El ejecutable se generará en: `Juego/Codigo/dist/Bossfight_ElTroyano.exe`

Después de compilar, usa `mover_exe.bat` para mover el `.exe` a la carpeta raíz del proyecto, donde los usuarios puedan acceder fácilmente.

**Configuración del Ícono:**

El script `create_icon.py` intentará usar sprites del juego para crear el ícono. Si quieres usar tu propia imagen:

1. Coloca tu imagen (PNG preferiblemente) en `Juego/assets/Sprites/`
2. Modifica `create_icon.py` para apuntar a tu imagen
3. Ejecuta el script de compilación

---

## 🎮 Controles

### Menús
| Tecla | Acción |
|-------|--------|
| `↑` `↓` o `W` `S` | Navegar opciones |
| `Enter` o `Espacio` o `X` | Seleccionar |
| `Esc` | Volver/Salir |

### Introducción (Top-Down)
| Tecla | Acción |
|-------|--------|
| `↑` `↓` `←` `→` o `W` `A` `S` `D` | Moverse |
| `X` o `Enter` | Interactuar con PC (iniciar batalla) |

### Batalla
| Tecla | Acción |
|-------|--------|
| `↑` `↓` `←` `→` | Mover el corazón (jugador) |
| `Z` o `Espacio` | Atacar al jefe |
| `Esc` | Pausar |

### Pantalla de Victoria
| Tecla | Acción |
|-------|--------|
| `Enter` o `Espacio` | Volver al menú |
| `Esc` | Salir del juego |

---

## 🔐 Código Secreto

¿Quieres acceder a todo el contenido sin desbloquear la dificultad Senior?

### 🎁 Truco: **UTNFRA**

**Cómo usarlo:**
1. Ve al menú principal
2. Escribe la palabra **UTNFRA** (sin necesidad de presionar Enter)
3. ¡Modo completo desbloqueado! ✨

Esto habilitará:
- ✅ Dificultad Senior inmediatamente
- ✅ Acceso a todas las fases en modo práctica
- ✅ Todas las estrellas obtenidas

> **Easter Egg**: Este código es un homenaje a la **Universidad Tecnológica Nacional - Facultad Regional Avellaneda**, donde nació este proyecto.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación principal
- **Pygame 2.0+**: Framework para desarrollo de videojuegos
- **Pillow (PIL)**: Manejo de imágenes y GIFs animados
- **OpenAI API**: Generación de diálogos dinámicos con GPT-3.5
- **Git**: Control de versiones

---

## 🎓 Objetivos Académicos

Este proyecto fue desarrollado como trabajo práctico integrador para demostrar:

1. **Programación Orientada a Objetos**: Clases, herencia, encapsulación
2. **Gestión de eventos**: Input del usuario, colisiones, timers
3. **Integración de APIs**: Conexión con servicios externos (OpenAI)
4. **Organización de código**: Modularización, separación de responsabilidades
5. **Manejo de archivos**: Carga de recursos multimedia
6. **Algoritmos y lógica**: Patrones de ataque, sistema de fases
7. **Documentación**: Comentarios, docstrings, README

---

## 📚 Mecánicas del Juego

### Sistema de Combate

- **Área de batalla**: Cuadro delimitado donde te mueves
- **Vida del jugador**: 100 HP (se reduce al recibir daño)
- **Vida del jefe**: 200 HP (3 fases a 66% y 33% de HP)
- **Bordes peligrosos**: Paredes rojas que aparecen aleatoriamente

### Patrones de Ataque

**Fase 1:**
- 🎯 Tutorial: Proyectiles simples
- 🌧️ Lluvia: Balas caen desde arriba
- ↗️ Diagonal: Ataque en ángulo
- ↔️ Lateral: Proyectiles horizontales
- 💥 Burst: Ráfagas direccionales

**Fase 2:**
- 🗡️ Lanzas: Proyectiles giratorios
- ⚔️ Tormenta de lanzas: Múltiples lanzas simultáneas

**Fase 3:**
- 🌀 Combinaciones letales: Todos los ataques anteriores
- ⭕ Círculos de proyectiles: Patrones concéntricos
- 🌊 Olas cruzadas: Ataques coordinados

### Sistema de Dificultad

- **Junior**: Velocidad estándar, ideal para principiantes
- **Senior**: +30% velocidad de proyectiles, para jugadores experimentados

---

---

## ❓ Solución de Problemas Comunes

### ❌ "ModuleNotFoundError: No module named 'pygame'"

**Solución:**
```bash
# Opción 1: Usar el instalador automático (Windows)
# Haz doble clic en: instalar_dependencias.bat

# Opción 2: Instalar manualmente
pip install -r requirements.txt

# Opción 3: Instalar solo lo básico
pip install pygame pillow
```

### ❌ "FileNotFoundError" o problemas con directorios de assets

**Solución:**
```bash
# IMPORTANTE: Ejecutar desde la carpeta correcta
cd Juego/Codigo
python main.py

# NO ejecutes desde la raíz del proyecto, debe ser desde Juego/Codigo
```

El juego busca los assets en rutas relativas. Si ejecutas desde otra carpeta, no encontrará los archivos.

### ❌ "No se cargan los GIFs animados"

**Solución:**
```bash
pip install pillow
```

Pillow es necesario para procesar GIFs animados (estrellas, fondos).

### ❌ "El juego no inicia o se cierra inmediatamente"

**Verificaciones:**
1. ¿Tienes Python 3.8 o superior? → `python --version`
2. ¿Instalaste las dependencias? → `pip list | findstr pygame`
3. ¿Estás en la carpeta correcta? → Debe ser `Juego/Codigo/`
4. ¿Hay errores en la consola? → Ejecuta con `python main.py` (no doble clic)

### ❌ "OpenAI API errors" o problemas con IA

**Solución:**
No te preocupes, el juego funciona perfectamente sin la API de OpenAI. Los diálogos usarán texto predefinido automáticamente. Si quieres usar la IA:

```bash
# Instalar biblioteca
pip install openai

# Configurar tu API key
# Windows PowerShell:
$env:OPENAI_API_KEY="tu-api-key-aqui"
```

### 💡 ¿Nada funciona? Usa el ejecutable

Si tienes muchos problemas con Python y las bibliotecas, simplemente usa el ejecutable:

👉 **Haz doble clic en `Bossfight_ElTroyano.exe`**

No requiere instalación de nada. ¡Funciona de inmediato!

---

## 🏆 Créditos

### Desarrollo
- **Desarrollador Principal**: Jeremías Fernández
- **GitHub**: [@JeremiasFernandez](https://github.com/JeremiasFernandez)

### Proyecto Académico
- **Institución**: Universidad Tecnológica Nacional - Facultad Regional Avellaneda (UTN FRA)
- **Materia**: Programación 1
- **Año**: 2024-2025

### Tecnologías
- **Pygame Community**: Framework de desarrollo
- **OpenAI**: API de inteligencia artificial
- **Python Software Foundation**: Lenguaje Python

### Inspiración
- **Undertale** (Toby Fox): Mecánicas de combate y estética
- **Bullet Hell Games**: Patrones de proyectiles

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

---

## 🐛 Problemas Conocidos y Soluciones

| Problema | Solución |
|----------|----------|
| El juego requiere los archivos de assets | ✅ Usar el `.exe` (assets incluidos) o ejecutar desde `Juego/Codigo/` |
| Integración con OpenAI requiere internet | ✅ El juego tiene diálogos offline por defecto |
| GIFs no se cargan | ✅ Instalar Pillow: `pip install pillow` |
| Errores de imports | ✅ Usar `instalar_dependencias.bat` o `pip install -r requirements.txt` |

**📖 Para más ayuda, consulta la [Sección de Solución de Problemas](#-solución-de-problemas-comunes)**

---

## 🔮 Futuras Mejoras

- [ ] Más fases del jefe
- [ ] Sistema de logros
- [ ] Cambiar skin del Mouse
- [ ] Un segundo jefe
- [ ] Mapa interactivo con parte de historia
- [ ] Distintos Finales
---

## 📞 Contacto

¿Tienes preguntas, sugerencias o encontraste un bug?

- **GitHub Issues**: [Reportar problema](https://github.com/JeremiasFernandez/Pygame-SimpleGame-Proyect/issues)
- **GitHub Profile**: [@JeremiasFernandez](https://github.com/JeremiasFernandez)
- **Email**: jereferdz@gmail.com

---

<div align="center">

**⭐ Si te gustó el proyecto, no olvides darle una estrella en GitHub ⭐**

Hecho con ❤️ y ☕ por estudiantes de la UTN FRA

</div>
