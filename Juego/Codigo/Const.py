
import pygame
import os

# Const.py
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 150, 255)
GRIS = (60, 60, 60)
AMARILLO = (255, 255, 0)

# Área de combate (importante para player.py)
BOX_X = 200
BOX_Y = 250
BOX_ANCHO = 400
BOX_ALTO = 300



pygame.font.init()
FUENTE_PRINCIPAL = pygame.font.Font(None, 36)


TITULO = "Bossfight: The virus"
VIDA_JUGADOR = 100


# --- Borde peligroso ---
BORDE_DURACION = 60              # frames (~1 seg)
BORDE_INTERVALO_MIN = 180        # frames mínimo (~3 seg)
BORDE_INTERVALO_MAX = 400        # frames máximo (~7 seg)
BORDE_DANO = 1                   # daño por tocarlo


# --- IA / Chat Configuration ---
# ⚠️ NUNCA subas tu API key al repositorio. Se usa variable de entorno.
# Para configurar: setx OPENAI_API_KEY "tu-clave-aqui" (en Windows)
# En Linux/Mac: export OPENAI_API_KEY="tu-clave-aqui"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

AI_PROVIDER = "openai"          # Futuro: permitir otros proveedores
AI_FALLBACK_ON_ERROR = True      # Si hay error o cuota excedida, usar respuestas simuladas
OPENAI_MODEL = "gpt-3.5-turbo"   # Modelo más barato: gpt-3.5-turbo ($0.0015 / 1K tokens)
OPENAI_MAX_TOKENS = 30           # Tokens máximos = respuesta más corta = más barato

# Personaliza el prompt del sistema para la IA
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



