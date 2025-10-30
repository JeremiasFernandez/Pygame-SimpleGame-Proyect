import pygame, random
import Const as c

class Border:
    """Clase que maneja el borde peligroso del campo de batalla."""

    def __init__(self):
        self.activo = False
        self.estado = "normal"  # "normal", "avisando", "dañino"
        self.timer = 0
        self.duracion = c.BORDE_DURACION
        self.intervalo = random.randint(c.BORDE_INTERVALO_MIN, c.BORDE_INTERVALO_MAX)
        self.color = c.GRIS

    def update(self, player):
        """Actualiza el estado del borde y aplica daño si corresponde."""
        self.timer += 1

        # --- Se activa aleatoriamente ---
        if not self.activo and self.timer >= self.intervalo:
            self.activo = True
            self.estado = "avisando"
            self.timer = 0
            self.duracion = c.BORDE_DURACION
            print("⚠️ El borde empieza a titilar...")

        # --- Fases ---
        if self.activo:
            self.duracion -= 1

            # FASE DE AVISO (titila rojo/blanco)
            if self.estado == "avisando":
                if (pygame.time.get_ticks() // 100) % 2 == 0:
                    self.color = c.ROJO
                else:
                    self.color = c.BLANCO

                if self.duracion <= 0:
                    self.estado = "dañino"
                    self.duracion = c.BORDE_DURACION
                    print("🔥 El borde se activa y hace daño!")

            # FASE DAÑINA (rojo fijo)
            elif self.estado == "dañino":
                self.color = c.ROJO

                # Aplicar daño si el jugador toca el borde
                if (player.rect.left <= c.BOX_X or
                    player.rect.right >= c.BOX_X + c.BOX_ANCHO or
                    player.rect.top <= c.BOX_Y or
                    player.rect.bottom >= c.BOX_Y + c.BOX_ALTO):
                    player.take_damage(c.BORDE_DANO)

                # Fin de la fase dañina
                if self.duracion <= 0:
                    self.reset()

        else:
            self.color = c.GRIS

    def reset(self):
        """Reinicia el evento."""
        self.activo = False
        self.estado = "normal"
        self.timer = 0
        self.duracion = c.BORDE_DURACION
        self.intervalo = random.randint(c.BORDE_INTERVALO_MIN, c.BORDE_INTERVALO_MAX)
        self.color = c.GRIS
        print("🟢 El borde vuelve a la normalidad")

    def draw(self, screen):
        """Dibuja el borde actual."""
        pygame.draw.rect(screen, self.color, (c.BOX_X, c.BOX_Y, c.BOX_ANCHO, c.BOX_ALTO), 2)
