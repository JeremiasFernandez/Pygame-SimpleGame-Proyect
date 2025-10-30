import pygame
import Const as c

class CombatSystem:
    def __init__(self):
        self.state = "menu"  # menu / ataque / defensa
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # 0 = Atacar, 1 = Objetos
        self.timer = 0

    def update(self, player, enemy):
        keys = pygame.key.get_pressed()

        # --- MENÚ PRINCIPAL ---
        if self.state == "menu":
            if keys[pygame.K_LEFT]:
                self.selected = 0
            if keys[pygame.K_RIGHT]:
                self.selected = 1
            if keys[pygame.K_x]:  # 👈 usar X en lugar de Enter
                if self.selected == 0:
                    self.state = "ataque"
                else:
                    player.hp = min(player.hp + 5, 20)
                    self.state = "defensa"
                    self.timer = 0

        # --- FASE DE ATAQUE (a definir) ---
        elif self.state == "ataque":
            # por ahora no hay minijuego, solo daño fijo
            enemy.hp -= 10
            print(f"⚔️ Ataque! HP enemigo: {enemy.hp}")
            self.state = "defensa"
            self.timer = 0

        # --- FASE DE DEFENSA (tu bossfight actual) ---
        elif self.state == "defensa":
            self.timer += 1
            # después de 5 segundos, volver al menú
            if self.timer > 5 * c.FPS:
                self.state = "menu"

    def draw(self, screen):
        # --- MENÚ ABAJO ---
        if self.state == "menu":
            opciones = ["ATACAR", "OBJETOS"]
            for i, texto in enumerate(opciones):
                color = c.AMARILLO if i == self.selected else c.BLANCO
                render = self.font.render(texto, True, color)
                rect = render.get_rect(center=(c.ANCHO // 2 + (i * 200) - 100, c.ALTO - 80))
                screen.blit(render, rect)

        elif self.state == "ataque":
            msg = self.font.render("¡ATACASTE!", True, c.ROJO)
            screen.blit(msg, (c.ANCHO // 2 - 80, c.ALTO - 100))
