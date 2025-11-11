"""
Const.py - Configuración Global del Juego
==========================================
Contiene todas las constantes y configuraciones del juego organizadas por categorías.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pygame
import os


# ============================================================================
# CONFIGURACIÓN DE PANTALLA
# ============================================================================
ANCHO = 800
ALTO = 600
FPS = 60


# ============================================================================
# PALETA DE COLORES
# ============================================================================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 150, 255)
GRIS = (60, 60, 60)
AMARILLO = (255, 255, 0)


# ============================================================================
# ÁREA DE COMBATE
# ============================================================================
# Define el rectángulo donde el jugador puede moverse durante el combate
BOX_X = 200
BOX_Y = 250
BOX_ANCHO = 400
BOX_ALTO = 300


# ============================================================================
# FUENTES Y TEXTO
# ============================================================================
pygame.font.init()
FUENTE_PRINCIPAL = pygame.font.Font(None, 36)


# ============================================================================
# CONFIGURACIÓN DEL JUEGO
# ============================================================================
TITULO = "Bossfight: The virus"
VIDA_JUGADOR = 100


# ============================================================================
# MECÁNICA DEL BORDE PELIGROSO
# ============================================================================
BORDE_DURACION = 60              # Duración en frames (~1 segundo)
BORDE_INTERVALO_MIN = 180        # Intervalo mínimo entre apariciones (~3 segundos)
BORDE_INTERVALO_MAX = 400        # Intervalo máximo entre apariciones (~7 segundos)
BORDE_DANO = 1                   # Daño por contacto con el borde


# ============================================================================
# CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL (CHAT)
# ============================================================================
# ⚠️ SEGURIDAD: Nunca subas tu API key al repositorio público
# La clave se obtiene desde una variable de entorno del sistema
#
# Configuración:
#   - Windows:    setx OPENAI_API_KEY "tu-clave-aqui"
#   - Linux/Mac:  export OPENAI_API_KEY="tu-clave-aqui"
#
# Luego reinicia la terminal/IDE para que la variable tome efecto

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Proveedor de IA (actualmente solo OpenAI, preparado para futuros proveedores)
AI_PROVIDER = "openai"

# Si hay error o cuota excedida, usar respuestas simuladas offline
AI_FALLBACK_ON_ERROR = True

# Modelo más económico: gpt-3.5-turbo ($0.0015 por 1K tokens)
OPENAI_MODEL = "gpt-3.5-turbo"

# Máximo de tokens por respuesta (respuestas más cortas = más barato)
OPENAI_MAX_TOKENS = 30

# Prompt del sistema que define la personalidad del virus
OPENAI_PROMPT = """Eres un virus maligno dentro de una computadora que está peleando contra el jugador.
Hablas de forma sarcástica, burlona y amenazante.
Eres ruso, mencionas a veces la tecnología rusa y el ciberespacio.
Respondes de forma muy corta (máximo 8 palabras).
Nunca sales del personaje.

El lore secreto del virus del que no debes casi mencionar, a no ser que sean mediante a pequeñas pistas, es el siguiente:
- Eres un virus informático avanzado creado por hackers rusos para infiltrarte en sistemas críticos.
- Tu objetivo es robar información sensible y causar caos en Argentina.
- Estas en medio de una guerra cibernética entre Rusia y el mundo entero
- Te enfrentas a un programador promedio que acaba de descubrirte.
"""



