import pygame, random, math
import Const as c
from characters.bullet import Bullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, bullets_group, all_sprites):
        super().__init__()
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites

        # ---------------- Core ----------------
        self.timer = 0
        self.attack_timer = 0
        self.attack_duration = 420          # ~7s a 60 FPS
        self.hp = 200
        self.phase = 1
        self.difficulty = 1.0               # escala velocidades/ritmos
        self.current_attack = "tutorial"    # siempre arranca suave
        self.music_playing = False          # control interno del boss (fase 2)
        self._phase2_entered = False
        self.phase2_music_started = False  # 👈 evita errores antes de la Fase 2


        # ---------------- Sprites ----------------
        # Fase 1 (virus)
        try:
            img1 = pygame.image.load("Juego/assets/sprites/Boss_Virus_1.png").convert_alpha()
        except:
            img1 = pygame.Surface((200, 200), pygame.SRCALPHA); img1.fill((220,220,220,255))
        self.image = pygame.transform.scale(img1, (200, 200))
        self.rect = self.image.get_rect(center=(c.ANCHO // 2, 140))

        # Fase 2 (troyano)
        try:
            img2 = pygame.image.load("Juego/assets/sprites/Boss_Virus_2.png").convert_alpha()
            self._phase2_img = pygame.transform.scale(img2, (200, 200))
        except:
            self._phase2_img = None

        # ---------------- Diálogo ----------------
        self.dialogo = None
        self.dialogo_timer = 0
        self.font = pygame.font.Font(None, 28)

        # ---------------- Rotación de ataques ----------------
        self.phase1_attacks = ["tutorial", "rain", "diagonal", "lateral1", "lateral2"]
        self.phase2_attacks = ["burst1", "burst2", "burst3", "spiral",
                               "diagonal", "rain", "lateral1", "lateral2",
                               "spears", "spearstorm"]
        self.special_attacks = ["burst1", "burst2", "burst3", "spiral", "spears"]
        self.special_chance = 0.25

        # ---------------- Fondo Fase 2 ----------------
        self.phase2_red_base = (54, 0, 0)   # #360000 muy oscuro
        self.particles = []                 # (x,y,dx,dy,size,life,color)

    # =========================================================
    #                        LOOP
    # =========================================================
    def update(self):
        self.timer += 1
        self.attack_timer += 1

        # --- Cambio automático de ataque ---
        if self.attack_timer >= self.attack_duration:
            self.cambiar_ataque()
            self.attack_timer = 0

        # --- FASE 1 ---
        if self.phase == 1:
            # ya no maneja música acá, solo ataques
            self.phase_one_behavior()

            if self.timer == 60:
                self.decir("JAJA, ¿crees que podés eliminarme?")
            if self.hp < 150 and not hasattr(self, "fase1_dialogo1"):
                self.decir("¡Ni siquiera estás en mi segunda fase!")
                self.fase1_dialogo1 = True

            if self.hp <= 100:
                self._enter_phase2()

        # --- FASE 2 ---
        elif self.phase == 2:
            self.phase_two_behavior()

            if not self.phase2_music_started:
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Juego/assets/Soundtrack/phase2.mp3")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print("🎵 Música: Phase 2 activada")
                    self.phase2_music_started = True
                except Exception as e:
                    print("⚠️ No se pudo reproducir música de fase 2:", e)

            if self.timer % 600 == 0:
                self.decir("¡NO PODÉS DERROTARME!")

        # --- Diálogo ---
        if self.dialogo_timer > 0:
            self.dialogo_timer -= 1
            if self.dialogo_timer <= 0:
                self.dialogo = None


    def _enter_phase2(self):
        """Transición limpia a la Fase 2."""
        if getattr(self, "_phase2_entered", False):
            return
        self._phase2_entered = True

        self.phase = 2
        self.image = pygame.image.load("Juego/assets/sprites/Boss_Virus_2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.difficulty = 1.4
        self.phase2_music_started = False  # 👈 se habilita para que update() la reproduzca
        self.decir("¡TE MOSTRARÉ MI VERDADERA FORMA!")


    # =========================================================
    #                   TRANSICIÓN FASE 2
    # =========================================================
    def _enter_phase2(self):
        if self._phase2_entered:
            return
        self._phase2_entered = True
        self.phase = 2
        self.music_playing = False  # permitimos que suene la de fase 2

        center = self.rect.center
        if self._phase2_img:
            self.image = self._phase2_img
        else:
            # fallback si no hay imagen
            surf = pygame.Surface((200,200), pygame.SRCALPHA)
            surf.fill((180, 60, 60, 255))
            self.image = surf
        self.rect = self.image.get_rect(center=center)

        # subir dificultad global (sin romper spearstorm lento)
        self.difficulty = 1.3
        self.decir("¡TE MOSTRARÉ MI VERDADERA FORMA!")

    # =========================================================
    #                    MÚSICA (segura)
    # =========================================================
    def play_music(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("⚠️ Error al reproducir música:", e)

    # =========================================================
    #                    ATAQUE ACTUAL
    # =========================================================
    def phase_one_behavior(self):
        getattr(self, f"attack_{self.current_attack}")()

    def phase_two_behavior(self):
        getattr(self, f"attack_{self.current_attack}")()

    # =========================================================
    #                ROTACIÓN DE ATAQUES
    # =========================================================
    def cambiar_ataque(self):
        # chance de especial (en cualquier fase)
        if random.random() < self.special_chance:
            self.current_attack = random.choice(self.special_attacks)
            self.decir("⚠️ ¡SISTEMA DE DEFENSA ACTIVADO!")
            return

        ataques = self.phase1_attacks if self.phase == 1 else self.phase2_attacks
        posibles = [a for a in ataques if a != self.current_attack]
        self.current_attack = random.choice(posibles)
        self.decir(f"¡MI ATAQUE {self.current_attack.upper()} TE ANIQUILARÁ!")

    # =========================================================
    #                    ATAQUES
    # =========================================================
    def attack_tutorial(self):
        """Lluvia lenta y suavecita (siempre el primero)."""
        if self.timer % 13 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 4)
            b.damage = 2
            self._spawn(b)

    def attack_rain(self):
        if self.timer % max(1, int(5 / self.difficulty)) == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, int(6 * self.difficulty))
            self._spawn(b)

    def attack_diagonal(self):
        if self.timer % max(1, int(4 / self.difficulty)) == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, int(5 * self.difficulty))
            b.speed_x = direction * int(3 * self.difficulty)
            b.speed_y = int(5 * self.difficulty)
            b.update = lambda b=b: self._move_diag(b)
            self._spawn(b)

    def attack_lateral1(self):
        """Desde la izquierda hacia la derecha."""
        if self.timer % max(1, int(13 / self.difficulty)) == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            b = Bullet(c.BOX_X, y, 0)
            b.speed_x = 6
            b.speed_y = 0
            b.damage = 3
            b.update = lambda b=b: self._move_diag(b)
            self._spawn(b)

    def attack_lateral2(self):
        """Desde la derecha hacia la izquierda."""
        if self.timer % max(1, int(13 / self.difficulty)) == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            b = Bullet(c.BOX_X + c.BOX_ANCHO, y, 0)
            b.speed_x = -6
            b.speed_y = 0
            b.damage = 3
            b.update = lambda b=b: self._move_diag(b)
            self._spawn(b)

    def attack_burst1(self):
        """Explosión circular (radial)."""
        if self.timer % 20 == 0:
            cx = c.ANCHO // 2
            cy = self.rect.centery + 20
            for ang in range(0, 360, 30):
                r = math.radians(ang)
                dx, dy = math.cos(r) * 4, math.sin(r) * 4
                b = Bullet(cx, cy, 0)
                b.damage = 4
                b.update = lambda b=b, dx=dx, dy=dy: self._move_vec(b, dx, dy)
                self._spawn(b)

    def attack_burst2(self):
        """Abanico frontal hacia abajo."""
        if self.timer % 25 == 0:
            cx = c.BOX_X + c.BOX_ANCHO // 2
            start = -60
            for i in range(5):
                ang = math.radians(start + i * 30)
                dx, dy = math.cos(ang) * 5, math.sin(ang) * 5
                b = Bullet(cx, c.BOX_Y + 40, 0)
                b.damage = 4
                b.update = lambda b=b, dx=dx, dy=dy: self._move_vec(b, dx, dy)
                self._spawn(b)

    def attack_burst3(self):
        """Tres ráfagas consecutivas al centro."""
        if self.timer % 90 < 15 and self.timer % 5 == 0:
            cx = c.BOX_X + c.BOX_ANCHO // 2
            for dx in [-4, -2, 0, 2, 4]:
                b = Bullet(cx, c.BOX_Y + 20, 6)
                b.speed_x = dx
                b.speed_y = 6
                b.damage = 5
                b.update = lambda b=b: self._move_diag(b)
                self._spawn(b)

    def attack_spiral(self):
        """Espiral vistosa (daño bajo)."""
        if self.timer % 15 == 0:
            cx, cy = c.ANCHO // 2, c.BOX_Y + 50
            for i in range(0, 360, 45):
                ang = math.radians(i + self.timer * 5)
                dx, dy = math.cos(ang) * 4, math.sin(ang) * 4
                b = Bullet(cx, cy, 0)
                b.damage = 2
                b.update = lambda b=b, dx=dx, dy=dy: self._move_vec(b, dx, dy)
                self._spawn(b)

    def attack_spears(self):
        """Lanzas (vertical u horizontal) más rápidas en F2."""
        if self.timer % max(1, int(40 / self.difficulty)) == 0:
            if random.choice([True, False]):  # vertical
                x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                b = Bullet(x, c.BOX_Y - 100, 0)
                b.image = pygame.Surface((10, 60), pygame.SRCALPHA); b.image.fill((200,200,255,230))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                b.speed_y = int(9 * self.difficulty)
                b.damage = 5
                b.update = lambda b=b: self._move_diag(b)
            else:  # horizontal
                y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                if random.choice([True, False]):
                    x, sx = c.BOX_X - 50, int(10 * self.difficulty)
                else:
                    x, sx = c.BOX_X + c.BOX_ANCHO + 50, -int(10 * self.difficulty)
                b = Bullet(x, y, 0)
                b.image = pygame.Surface((60, 10), pygame.SRCALPHA); b.image.fill((200,200,255,230))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = sx
                b.damage = 5
                b.update = lambda b=b: self._move_diag(b)
            self._spawn(b)

    def attack_spearstorm(self):
        """MUCHAS lanzas MUY LENTAS a la vez (espectáculo)."""
        if self.timer % 90 == 0:  # “oleadas” periódicas
            cantidad = random.randint(12, 18)
            for _ in range(cantidad):
                if random.choice([True, False]):  # vertical lenta
                    x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                    b = Bullet(x, c.BOX_Y - 100, 0)
                    b.image = pygame.Surface((10, 70), pygame.SRCALPHA); b.image.fill((170, 200, 255, 230))
                    b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                    b.speed_y = 2  # MUY lenta
                    b.damage = 4
                    b.update = lambda b=b: self._move_diag(b)
                else:  # horizontal lenta
                    y = random.randint(c.BOX_Y + 30, c.BOX_Y + c.BOX_ALTO - 30)
                    if random.choice([True, False]):
                        x, sx = c.BOX_X - 60, 2
                    else:
                        x, sx = c.BOX_X + c.BOX_ANCHO + 60, -2
                    b = Bullet(x, y, 0)
                    b.image = pygame.Surface((70, 10), pygame.SRCALPHA); b.image.fill((170, 200, 255, 230))
                    b.rect = b.image.get_rect(center=(x, y))
                    b.speed_x = sx
                    b.damage = 4
                    b.update = lambda b=b: self._move_diag(b)
                self._spawn(b)

    # =========================================================
    #                   MOVIMIENTOS & SPAWN
    # =========================================================
    def _spawn(self, bullet):
        self.bullets_group.add(bullet)
        self.all_sprites.add(bullet)

    def _move_diag(self, b):
        b.rect.y += getattr(b, "speed_y", 0)
        b.rect.x += getattr(b, "speed_x", 0)
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
            b.rect.right < 0 or b.rect.left > c.ANCHO):
            b.kill()

    def _move_vec(self, b, dx, dy):
        b.rect.x += dx
        b.rect.y += dy
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
            b.rect.right < 0 or b.rect.left > c.ANCHO):
            b.kill()

    # =========================================================
    #                   UI: BARRA & DIÁLOGO
    # =========================================================
    def draw_health_bar(self, screen):
        vida_max = 200
        vida_actual = max(0, self.hp)
        barra_ancho, barra_alto = 250, 15
        barra_x = (c.ANCHO // 2) - (barra_ancho // 2)
        barra_y = 30
        propor = vida_actual / vida_max
        relleno = int(barra_ancho * propor)

        pygame.draw.rect(screen, c.GRIS,  (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, c.ROJO,  (barra_x, barra_y, relleno,     barra_alto))
        pygame.draw.rect(screen, c.BLANCO,(barra_x, barra_y, barra_ancho, barra_alto), 2)

        f = pygame.font.Font(None, 28)
        t = f.render(f"{vida_actual}/{vida_max}", True, c.BLANCO)
        screen.blit(t, t.get_rect(center=(c.ANCHO // 2, barra_y + barra_alto // 2)))

    def decir(self, texto, duracion=150):
        self.dialogo = texto
        self.dialogo_timer = duracion

    def draw_dialogue(self, screen):
        if not self.dialogo: return
        text_surf = self.font.render(self.dialogo, True, c.BLANCO)
        rect = text_surf.get_rect(center=(c.ANCHO // 2, self.rect.bottom + 30))
        screen.blit(text_surf, rect)

    # =========================================================
    #             FONDO FASE 2 (detrás del borde)
    # =========================================================
    def draw_phase2_background(self, screen):
        """Llamar desde main ANTES de dibujar el borde. Solo fase 2."""
        if self.phase != 2:
            return

        # capa base rojiza MUY oscura
        base = pygame.Surface((c.ANCHO, c.ALTO), pygame.SRCALPHA)
        base.fill((*self.phase2_red_base, 230))  # casi negro con leve rojo
        screen.blit(base, (0, 0))

        # partículas (amarillas para que se vean)
        if random.random() < 0.25:
            # nace fuera del área del cuadro para no “ensuciar” adentro
            while True:
                x = random.randint(0, c.ANCHO)
                y = random.randint(0, c.ALTO)
                if not (c.BOX_X < x < c.BOX_X + c.BOX_ANCHO and c.BOX_Y < y < c.BOX_Y + c.BOX_ALTO):
                    break
            dx = random.uniform(-0.4, 0.4)
            dy = random.uniform(-1.0, -0.3)
            size = random.randint(1, 2)
            life = random.randint(60, 120)
            color = (255, 230, 120)  # amarillitas
            self.particles.append([x, y, dx, dy, size, life, color])

        # actualizar/dibujar
        alive = []
        for (x, y, dx, dy, size, life, color) in self.particles:
            x += dx; y += dy; life -= 1
            if life > 0:
                alpha = max(0, min(180, life + 60))
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, alpha), (size, size), size)
                screen.blit(s, (x, y))
                alive.append([x, y, dx, dy, size, life, color])
        self.particles = alive


    def draw_health_bar(self, screen):
        vida_max = 200
        vida_actual = max(0, self.hp)

        barra_ancho = 250
        barra_alto = 15
        barra_x = (c.ANCHO // 2) - (barra_ancho // 2)
        barra_y = 30

        proporcion = vida_actual / vida_max
        ancho_relleno = int(barra_ancho * proporcion)

        pygame.draw.rect(screen, c.GRIS, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, c.ROJO, (barra_x, barra_y, ancho_relleno, barra_alto))
        pygame.draw.rect(screen, c.BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)

        font = pygame.font.Font(None, 28)
        texto = font.render(f"{vida_actual}/{vida_max}", True, c.BLANCO)
        rect = texto.get_rect(center=(c.ANCHO // 2, barra_y + barra_alto // 2))
        screen.blit(texto, rect)

    # --------------------------------------------
    def cambiar_ataque(self):
        if random.random() < self.special_chance:
            self.current_attack = random.choice(self.special_attacks)
            self.decir("⚠️ ¡SISTEMA DE DEFENSA ACTIVADO!")
            return

        ataques = self.phase1_attacks if self.phase == 1 else self.phase2_attacks
        posibles = [atk for atk in ataques if atk != self.current_attack]
        self.current_attack = random.choice(posibles)
        self.decir(f"¡MI ATAQUE {self.current_attack.upper()} TE ANIQUILARÁ!")

    # --------------------------------------------
    def phase_one_behavior(self):
        getattr(self, f"attack_{self.current_attack}")()

    def phase_two_behavior(self):
        getattr(self, f"attack_{self.current_attack}")()

    # --------------------------------------------
    def play_music(self, ruta):
        """Reproduce música si no está ya sonando esa misma pista."""
        try:
            # si no hay música o cambió la pista
            if not pygame.mixer.music.get_busy() or getattr(self, "current_track", None) != ruta:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.55)
                pygame.mixer.music.play(-1)
                self.current_track = ruta
                print(f"🎵 Reproduciendo música de fase 2: {ruta}")
        except Exception as e:
            print(f"⚠️ Error al reproducir la música de fase 2: {e}")


    # --------------------------------------------
    def draw_title(self, screen):
        """Título dramático solo en fase 2"""
        if self.show_title and self.title_timer > 0:
            self.title_timer -= 1
            self.title_wave += 0.15

            offset_y = math.sin(self.title_wave) * 3
            text = self.title_font.render("TROYANO LEGENDARIO", True, (255, 220, 220))
            alpha = max(0, int(255 * (self.title_timer / 240)))
            text.set_alpha(alpha)

            rect = text.get_rect(center=(c.ANCHO // 2, self.rect.top - 40 + offset_y))
            screen.blit(text, rect)

            if self.title_timer <= 0:
                self.show_title = False


    # --------------------------------------------
    #                ATAQUES
    # --------------------------------------------
    def attack_tutorial(self):
        if self.timer % 13 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 4)
            b.damage = 1
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_rain(self):
        step = max(1, int(5 / self.difficulty))
        if self.timer % step == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(6 * self.difficulty)))
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_diagonal(self):
        step = max(1, int(4 / self.difficulty))
        if self.timer % step == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(5 * self.difficulty)))
            b.speed_x = direction * max(1, int(3 * self.difficulty))
            b.speed_y = max(1, int(5 * self.difficulty))
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_lateral1(self):
        step = max(1, int(13 / self.difficulty))
        if self.timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X
            dx = max(1, int(6 * self.difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 2
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_lateral2(self):
        step = max(1, int(13 / self.difficulty))
        if self.timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X + c.BOX_ANCHO
            dx = -max(1, int(6 * self.difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 2
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_burst1(self):
        if self.timer % 20 == 0:
            center_x = c.ANCHO // 2
            center_y = self.rect.centery + 20
            for angle_deg in range(0, 360, 30):
                angle = math.radians(angle_deg)
                dx = math.cos(angle) * max(2, 4 * self.difficulty / 1.8)
                dy = math.sin(angle) * max(2, 4 * self.difficulty / 1.8)
                b = Bullet(center_x, center_y, 0)
                b.damage = 2
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_burst2(self):
        if self.timer % 25 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            start_angle = -60
            for i in range(5):
                angle = math.radians(start_angle + i * 30)
                dx = math.cos(angle) * max(2, 5 * self.difficulty / 1.8)
                dy = math.sin(angle) * max(2, 5 * self.difficulty / 1.8)
                b = Bullet(center_x, c.BOX_Y + 40, 0)
                b.damage = 2
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_burst3(self):
        # tres ráfagas cortas seguidas
        if self.timer % 90 < 15 and self.timer % 5 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            for dx in [-4, -2, 0, 2, 4]:
                b = Bullet(center_x, c.BOX_Y + 20, max(1, int(6 * self.difficulty)))
                b.speed_x = int(dx * self.difficulty)
                b.speed_y = max(1, int(6 * self.difficulty))
                b.damage = 2
                b.update = lambda b=b: self.move_diagonal(b)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_spiral(self):
        if self.timer % 15 == 0:
            center_x = c.ANCHO // 2
            center_y = c.BOX_Y + 50
            for i in range(0, 360, 45):
                angle = math.radians(i + self.timer * 5)
                dx = math.cos(angle) * max(2, 4 * self.difficulty / 1.8)
                dy = math.sin(angle) * max(2, 4 * self.difficulty / 1.8)
                b = Bullet(center_x, center_y, 0)
                b.damage = 2
                b.update = lambda dx=dx, dy=dy, b=b: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_spears(self):
        """Lanzas largas verticales u horizontales (más duras en fase 2)."""
        step = max(1, int(40 / self.difficulty))
        if self.timer % step == 0:
            orientacion = random.choice(["vertical", "horizontal"])

            if orientacion == "vertical":
                x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                b = Bullet(x, c.BOX_Y - 100, 0)
                # superficie alargada (convert_alpha para blend)
                b.image = pygame.Surface((10, 80), pygame.SRCALPHA).convert_alpha()
                b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                b.speed_y = max(2, int(9 * self.difficulty))
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)

            else:
                y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                lado = random.choice(["izq", "der"])
                if lado == "izq":
                    x = c.BOX_X - 60
                    dx = max(2, int(10 * self.difficulty))
                else:
                    x = c.BOX_X + c.BOX_ANCHO + 60
                    dx = -max(2, int(10 * self.difficulty))

                b = Bullet(x, y, 0)
                b.image = pygame.Surface((80, 10), pygame.SRCALPHA).convert_alpha()
                b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = dx
                b.damage = 4
                b.update = lambda b=b: self.move_diagonal(b)

            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_spearstorm(self):
        """Tormenta de lanzas lentas: salen muchas constantemente, muy despacio."""
        # genera muchas lanzas lentamente cada frame
        if self.timer % 80 == 0:  # 👈 cada pocos frames (ajustable)
            cantidad = random.randint(3, 6)  # 👈 varias lanzas por tick

            for _ in range(cantidad):
                orientacion = random.choice(["vertical", "horizontal"])

                if orientacion == "vertical":
                    # Lanza que cae desde arriba muy despacio
                    x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                    b = Bullet(x, c.BOX_Y - 100, 0)
                    b.image = pygame.Surface((10, 70), pygame.SRCALPHA).convert_alpha()
                    b.image.fill((180, 200, 255, 220))  # un poco translúcida
                    b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                    b.speed_y = random.uniform(0.5, 1.2)  # 👈 super lenta
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)

                else:
                    # Lanza lateral muy lenta
                    y = random.randint(c.BOX_Y + 30, c.BOX_Y + c.BOX_ALTO - 30)
                    lado = random.choice(["izq", "der"])
                    if lado == "izq":
                        x = c.BOX_X - 60
                        dx = random.uniform(0.5, 1.2)
                    else:
                        x = c.BOX_X + c.BOX_ANCHO + 60
                        dx = -random.uniform(0.5, 1.2)

                    b = Bullet(x, y, 0)
                    b.image = pygame.Surface((70, 10), pygame.SRCALPHA).convert_alpha()
                    b.image.fill((180, 200, 255, 220))
                    b.rect = b.image.get_rect(center=(x, y))
                    b.speed_x = dx
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)

                self.bullets_group.add(b)
                self.all_sprites.add(b)


    # --------------------------------------------
    def move_diagonal(self, b):
        b.rect.y += getattr(b, "speed_y", 0)
        b.rect.x += getattr(b, "speed_x", 0)
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
            b.rect.right < 0 or b.rect.left > c.ANCHO):
            b.kill()
    def move_spiral(self, b, dx, dy):
        b.rect.x += dx
        b.rect.y += dy
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
            b.rect.right < 0 or b.rect.left > c.ANCHO):
            b.kill()
    # --------------------------------------------
    # --------------------------------------------
    #           DIÁLOGO DEL JEFE
    # --------------------------------------------
    def decir(self, texto, duracion=150):
        """Muestra un diálogo temporal del jefe."""
        self.dialogo = texto
        self.dialogo_timer = duracion

    def draw_dialogue(self, screen):
        """Dibuja el texto de diálogo si está activo."""
        if hasattr(self, "dialogo") and self.dialogo:
            text_surf = self.font.render(self.dialogo, True, (255, 255, 255))
            rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom + 30))
            screen.blit(text_surf, rect)
