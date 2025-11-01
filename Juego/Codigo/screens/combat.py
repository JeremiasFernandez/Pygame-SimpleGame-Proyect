import pygame
import random
import Const as c
import os

class AttackEffect(pygame.sprite.Sprite):
    def __init__(self, enemy_rect):
        super().__init__()
        self.frames = []
        slash_path = os.path.join("Juego", "assets", "Sprites", "slash.gif")
        self.load_frames(slash_path)
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=enemy_rect.center)
        self.timer = 0
        self.frame_duration = 6
        self.finished = False

    def load_frames(self, path):
        gif = pygame.image.load(path).convert_alpha()
        width = gif.get_width() // 6
        height = gif.get_height()
        for i in range(6):
            frame = gif.subsurface((i * width, 0, width, height))
            self.frames.append(pygame.transform.scale(frame, (200, 200)))

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.current_frame]


class CombatSystem:
    def __init__(self):
        self.state = "menu"
        # Volver a la fuente por defecto usada antes
        self.font = pygame.font.Font(None, 36)
        self.selected = 0
        self.timer = 0
        self.DEFENSA_DUR = int(10 * 60)

        self._x_prev = False
        self._left_prev = False
        self._right_prev = False

        try:
            self.attack_sound = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "Attack.wav"))
            self.attack_sound.set_volume(0.5)
        except Exception as e:
            self.attack_sound = None
            print(f"❌ No se pudo cargar Attack.wav: {e}")

        try:
            self.curarse_sound = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "healup.mp3"))
            self.curarse_sound.set_volume(0.2)
        except Exception as e:
            self.curarse_sound = None
            print(f"❌ No se pudo cargar healup.mp3: {e}")

        self.attack_effect = None
        self.enemy_shake_timer = 0
        self.enemy_base_pos = None

        # --- Diálogos de menú ---
        # Agrega aquí todos los textos que quieras que aparezcan aleatoriamente al entrar al menú.
        self.menu_dialogues = [
            "Atacar o curarse?",
            "Eliminar el virus te llena de determinacion",
            "El virus te está observando",
            "Un golpe menos",
            "El Virus busca venganza",
            "Tu computadora no sanara sola",
            "Tratas de comprender la figura del enemigo",
            "El enemigo te clava la mirada",
            "Preferirias estar en la cama",
            "No aprobaras el examen si no lo eliminas",
            "Te sientes debil",
            "El virus hace poses extrañas",
            "El virus baila samba",
            "El virus esta burlando de tu nota de programacion",
            "Se nota que no es tu primer intento",
            "TLauncher te esta observando",
            "Saludos a la UTN",
            "Pulsa la X si queres",
            "Spyware detected",
            "El virus se aburre y mira TikTok",
            "Cick, Click",
            "Vos podes",
            "...",
            "....",
            ".....",
            "¿Dificil?",
            "El enemigo se ve pensativo",
            "El enemigo golpea al piso",
            "¿Virtual o real?,"
            "¡Cuidado con el borde!"
            ""
        ]
        self._menu_dialog_current = None
        self._menu_dialog_color = (240, 240, 255)
        self._menu_dialog_margin = 14

        # Seleccionar diálogo para el primer menú
        self._pick_menu_dialog()

    def _pick_menu_dialog(self):
        if not self.menu_dialogues:
            self._menu_dialog_current = None
            return
        self._menu_dialog_current = random.choice(self.menu_dialogues)

    

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def enter_menu(self):
        self.state = "menu"
        self._pick_menu_dialog()

    def _pressed_once(self, now, prev_attr):
        prev = getattr(self, prev_attr)
        setattr(self, prev_attr, now)
        return now and not prev

    def update(self, player, enemy):
        keys = pygame.key.get_pressed()

        left_once = self._pressed_once(keys[pygame.K_LEFT], "_left_prev")
        right_once = self._pressed_once(keys[pygame.K_RIGHT], "_right_prev")
        x_once = self._pressed_once(keys[pygame.K_x], "_x_prev")

        if self.state == "menu":
            if left_once:
                self.selected = 0
            if right_once:
                self.selected = 1

            if x_once:
                if self.selected == 0:
                    if self.attack_sound:
                        print("▶️ Reproduciendo Attack.wav")
                        self.attack_sound.play()
                    if enemy:
                        self.attack_effect = AttackEffect(enemy.rect)
                        self.enemy_shake_timer = 10
                        self.enemy_base_pos = enemy.rect.topleft
                        # Use enemy.hit so phase transitions and side-effects run
                        try:
                            enemy.hit()
                        except Exception:
                            # Fallback to direct HP decrement if method missing
                            enemy.hp -= 10
                    self.state = "ataque"
                else:
                    player.hp = min(player.hp + 15, 20)
                    if self.curarse_sound:
                        print("▶️ Reproduciendo healup.mp3")
                        self.curarse_sound.play()
                    else:
                        print("❌ No se pudo reproducir healup.mp3")
                    self.state = "defensa"
                    self.timer = 0

        elif self.state == "ataque":
            if hasattr(enemy, 'silencio_activo') and enemy.silencio_activo:
                return
            if self.attack_effect:
                self.attack_effect.update()
                if self.attack_effect.finished:
                    self.attack_effect = None
                    self.state = "defensa"
                    self.timer = 0
            else:
                self.state = "defensa"
                self.timer = 0

        elif self.state == "defensa":
            self.timer += 1
            if self.timer >= self.DEFENSA_DUR:
                self.enter_menu()

        if self.enemy_shake_timer > 0 and enemy:
            offset = (-2, 2)[self.enemy_shake_timer % 2]
            enemy.rect.topleft = (self.enemy_base_pos[0] + offset, self.enemy_base_pos[1])
            self.enemy_shake_timer -= 1
            if self.enemy_shake_timer == 0:
                enemy.rect.topleft = self.enemy_base_pos

    def draw(self, screen, enemy=None):
        if self.state == "menu":
            opciones = ["ATACAR", "CURARSE"]
            for i, texto in enumerate(opciones):
                color = c.AMARILLO if i == self.selected else c.BLANCO
                render = self.font.render(texto, True, color)
                rect = render.get_rect(center=(c.ANCHO // 2 + (i * 200) - 100, c.ALTO - 80))
                screen.blit(render, rect)

            # Dibujar diálogo de menú dentro del border
            if self._menu_dialog_current:
                max_w = c.BOX_ANCHO - self._menu_dialog_margin * 2
                lines = self._wrap_text(self._menu_dialog_current, self.font, max_w)
                # Caja de fondo sutil
                box_h = 8 + len(lines) * (self.font.get_height() + 2)
                box_rect = pygame.Rect(c.BOX_X + self._menu_dialog_margin,
                                       c.BOX_Y + self._menu_dialog_margin,
                                       max_w,
                                       box_h)
                bg = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                bg.fill((10, 10, 30, 120))
                screen.blit(bg, box_rect.topleft)
                # Texto
                y = box_rect.top + 4
                for ln in lines:
                    surf = self.font.render(ln, True, self._menu_dialog_color)
                    screen.blit(surf, (box_rect.left + 4, y))
                    y += self.font.get_height() + 2

        elif self.state == "ataque":
            if enemy and hasattr(enemy, 'silencio_activo') and enemy.silencio_activo:
                return
            msg = self.font.render("¡ATACASTE!", True, c.ROJO)
            screen.blit(msg, (c.ANCHO // 2 - 80, c.ALTO - 100))

        if self.attack_effect:
            screen.blit(self.attack_effect.image, self.attack_effect.rect)
