import pygame
import Const as c

class CombatSystem:
    def __init__(self):
        # Estados: "menu" / "ataque" / "defensa"
        self.state = "menu"
        self.font = pygame.font.Font(None, 36)
        self.selected = 0  # 0 = Atacar, 1 = Objetos

        # control temporal para "defensa"
        self.timer = 0
        self.DEFENSA_DUR = int(10 * 60)  # 3s a 60 FPS (ajustá a gusto)

        # edge detection para teclas
        self._x_prev = False
        self._left_prev = False
        self._right_prev = False

        # SFX ataque (opcional)
        try:
            self.attack_sound = pygame.mixer.Sound("Juego/assets/Soundtrack/attack.wav")
            self.attack_sound.set_volume(0.5)
        except:
            self.attack_sound = None
            print("⚠️ No se pudo cargar el sonido de ataque.")

    def _pressed_once(self, now, prev_attr):
        prev = getattr(self, prev_attr)
        setattr(self, prev_attr, now)
        return now and not prev

    def update(self, player, enemy):
        keys = pygame.key.get_pressed()

        left_once  = self._pressed_once(keys[pygame.K_LEFT],  "_left_prev")
        right_once = self._pressed_once(keys[pygame.K_RIGHT], "_right_prev")
        x_once     = self._pressed_once(keys[pygame.K_x],     "_x_prev")

        # --- MENÚ ---
        if self.state == "menu":
            if left_once:
                self.selected = 0
            if right_once:
                self.selected = 1

            if x_once:
                if self.selected == 0:       # ATACAR
                    self.state = "ataque"
                else:                         # OBJETOS
                    player.hp = min(player.hp + 15, 20)
                    self.state = "defensa"
                    self.timer = 0

        # --- ATAQUE (placeholder sin minijuego) ---
        elif self.state == "ataque":
            if self.attack_sound:
                self.attack_sound.play()
            if enemy:  # por si acaso
                enemy.hp -= 10
            # Pasamos a DEFENSA (esquivar balas del boss) self.DEFENSA_DUR
            self.state = "defensa"
            self.timer = 0

        # --- DEFENSA (tu bossfight actual) ---
        elif self.state == "defensa":
            self.timer += 1
            # cuando termina la “oleada”, volvemos al menú
            if self.timer >= self.DEFENSA_DUR:
                self.state = "menu"

    def draw(self, screen):
        # Menú abajo (sin player)
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

        # En "defensa" no dibujamos UI extra (se ve la batalla)  defensa

