
import pygame

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



