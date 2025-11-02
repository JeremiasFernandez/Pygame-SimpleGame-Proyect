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

        # --- Barra de tiempo de defensa ---
        self.defense_bar_height = 4  # línea delgada
        self.defense_bar_margin = 8  # píxeles por encima del border
        self.defense_bar_bg = (40, 40, 60, 160)  # fondo semi-transparente
        self.defense_bar_fg = (232, 232, 232)      # color de la barra (restante)

        # --- Sprites para botones de menú (50x23) ---
        self.atacar_normal = None
        self.atacar_selected = None
        self.curarse_normal = None
        self.curarse_selected = None
        
        try:
            atacar_n_path = os.path.join("Juego", "assets", "Sprites", "atacar_normal.png")
            self.atacar_normal = pygame.image.load(atacar_n_path).convert_alpha()
            self.atacar_normal = pygame.transform.scale(self.atacar_normal, (100, 46))
            print(f"✅ Sprite atacar_normal cargado: {atacar_n_path}")
        except Exception:
            print("ℹ️  atacar_normal.png no encontrado; usando texto")
        
        try:
            atacar_s_path = os.path.join("Juego", "assets", "Sprites", "atacar_selected.png")
            self.atacar_selected = pygame.image.load(atacar_s_path).convert_alpha()
            self.atacar_selected = pygame.transform.scale(self.atacar_selected, (100, 46))
            print(f"✅ Sprite atacar_selected cargado: {atacar_s_path}")
        except Exception:
            print("ℹ️  atacar_selected.png no encontrado; usando texto")
        
        try:
            curarse_n_path = os.path.join("Juego", "assets", "Sprites", "curarse_normal.png")
            self.curarse_normal = pygame.image.load(curarse_n_path).convert_alpha()
            self.curarse_normal = pygame.transform.scale(self.curarse_normal, (100, 46))
            print(f"✅ Sprite curarse_normal cargado: {curarse_n_path}")
        except Exception:
            print("ℹ️  curarse_normal.png no encontrado; usando texto")
        
        try:
            curarse_s_path = os.path.join("Juego", "assets", "Sprites", "curarse_selected.png")
            self.curarse_selected = pygame.image.load(curarse_s_path).convert_alpha()
            self.curarse_selected = pygame.transform.scale(self.curarse_selected, (100, 46))
            print(f"✅ Sprite curarse_selected cargado: {curarse_s_path}")
        except Exception:
            print("ℹ️  curarse_selected.png no encontrado; usando texto")

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
            "¡Cuidado con el borde!",
            "El enemigo te muestra sus músculos",
            "Te falta odio",
            "El enemigo se ríe de ti",
            "Windows defender was disabled",
            "Pensaste que era un problema, pero era yo, el virus!",
            "El virus entro a %%APPDATA%%",
            "El virus se burla de tu falta de atención",
            "El virus: ez",
            "El virus: so easy",
            "El virus: gg no player",
            "El virus: Casi uso las manos",
            "El virus: ¿como se le sube la dificultad al bot?",
            "La oscuridad revela la luz",
            "El dolor forja la fuerza",
            "La derrota es solo un paso hacia la victoria",
            "Tu vida: 3hp",
            "Tu determinacion: 15%",
            "Intentos: 67",
            "desinstalando Linkedin...",
            "Un gmail ha llegado: 'Felicidades has ganado un premio!!'"
            "Notificacion recibida: 'Если вы это читаете, вы молодец.' "

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
            
            # Determinar qué sprites usar
            sprites = [
                (self.atacar_selected if self.selected == 0 else self.atacar_normal),
                (self.curarse_selected if self.selected == 1 else self.curarse_normal)
            ]
            
            for i, (texto, sprite) in enumerate(zip(opciones, sprites)):
                x = c.ANCHO // 2 + (i * 200) - 100
                y = c.ALTO - 80
                
                # Si el sprite existe, dibujarlo; si no, usar texto
                if sprite:
                    sprite_rect = sprite.get_rect(center=(x, y))
                    screen.blit(sprite, sprite_rect)
                else:
                    # Fallback a texto
                    color = c.AMARILLO if i == self.selected else c.BLANCO
                    render = self.font.render(texto, True, color)
                    rect = render.get_rect(center=(x, y))
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

    def draw_defense_timer_bar(self, screen: pygame.Surface):
        """Dibuja una barra delgada arriba del border que se achica con el tiempo de defensa restante."""
        # Calcular progreso restante (1.0 -> 0.0)
        dur = max(1, getattr(self, 'DEFENSA_DUR', 1))
        t = max(0, min(self.timer, dur))
        frac_left = 1.0 - (t / dur)

        # Geometría de la barra
        full_w = c.BOX_ANCHO
        bar_w = int(full_w * frac_left)
        bar_h = self.defense_bar_height
        x = c.BOX_X
        y = max(0, c.BOX_Y - self.defense_bar_margin - bar_h)

        # Fondo (track) semi-transparente del ancho completo
        track = pygame.Surface((full_w, bar_h), pygame.SRCALPHA)
        track.fill(self.defense_bar_bg)
        screen.blit(track, (x, y))

        # Barra restante (se achica con el tiempo)
        if bar_w > 0:
            rect_fg = pygame.Rect(x, y, bar_w, bar_h)
            pygame.draw.rect(screen, self.defense_bar_fg, rect_fg)
