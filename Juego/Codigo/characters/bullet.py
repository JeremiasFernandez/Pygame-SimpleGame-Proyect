"""bullet.py - Clean implementation of Bullet and AttackManager

All attack methods accept (timer=0, difficulty=1.0) to match Boss calls.
Uses AttackManager.spawn() to properly add bullets to groups.
"""

import pygame
import os
import random
import math
import Const as c

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=0):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.image.fill(c.BLANCO)
        self.rect = self.image.get_rect(center=(x, y))
        # Default vertical movement 
        self.speed = speed
        # Optional vector movement
        self.speed_x = 0 
        self.speed_y = 0
        # Default ignore border
        self.ignore_border = True
        # Sub-pixel position (para velocidades < 1 px/frame)
        self.fx = float(self.rect.centerx)
        self.fy = float(self.rect.centery)

    def update(self):
        """Combined default vertical speed + vector movement if set (sub-pixel)."""
        # Acumular en coordenadas flotantes
        self.fx += float(self.speed_x)
        self.fy += float(self.speed_y) + float(self.speed)
        # Aplicar al rect (centro) redondeando
        self.rect.center = (int(self.fx), int(self.fy))
        # Remove if outside screen
        if (self.rect.top > c.ALTO or self.rect.bottom < 0 or
                self.rect.left > c.ANCHO or self.rect.right < 0):
            self.kill()

class AttackManager:
    def __init__(self, boss, bullets_group, all_sprites=None):
        self.boss = boss
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites

        # --- Simple Bullet sprite (for normal bullets) --- speed

        self.simplebullet10 = None  # 10x10 preescalado
        try:
            sb_path = os.path.join("Juego", "assets", "Sprites", "simplebullet.png")
            sb_base = pygame.image.load(sb_path).convert_alpha()
            self.simplebullet10 = pygame.transform.smoothscale(sb_base, (10, 10))
            print(f"🔸 simplebullet cargado: {sb_path}")
        except Exception:
            # Fallback: se usará el cuadrado blanco por defecto del Bullet
            print("ℹ️  simplebullet.png no encontrado; usando forma por defecto para balas simples")

        # Preload optional spear sprites in all directions (falls back to rectangles if missing)
        # Base spear.png is assumed to point UP; we derive DOWN/LEFT/RIGHT by rotation.
        self.spear_u80 = self.spear_d80 = self.spear_l80 = self.spear_r80 = None
        self.spear_u70 = self.spear_d70 = self.spear_l70 = self.spear_r70 = None
        # Optional big ball sprite for phase 3 circle attack
        self.ballcircle50 = None

        try:
            spear_path = os.path.join("Juego", "assets", "Sprites", "spear.png")
            base = pygame.image.load(spear_path).convert_alpha()
            # Build UP baseline sizes (keep width=12 to match current visuals)
            self.spear_u80 = pygame.transform.smoothscale(base, (12, 80))
            self.spear_u70 = pygame.transform.smoothscale(base, (12, 70))
            # Derive the other directions by rotation
            self.spear_d80 = pygame.transform.rotate(self.spear_u80, 180)
            self.spear_r80 = pygame.transform.rotate(self.spear_u80, -90)
            self.spear_l80 = pygame.transform.rotate(self.spear_u80, 90)
            self.spear_d70 = pygame.transform.rotate(self.spear_u70, 180)
            self.spear_r70 = pygame.transform.rotate(self.spear_u70, -90)
            self.spear_l70 = pygame.transform.rotate(self.spear_u70, 90)
            print(f"🗡️  Spear sprite cargado y orientaciones generadas: {spear_path}")
        except Exception:
            # No sprite available; rectangular fallback will be used
            print("⚠️  Spear sprite no encontrado, usando rectángulos (buscado spear.png en Juego/assets/Sprites)")

        # --- Sprite y sonido para indicador de spearcross ---
        self.spearcross_indicator = None
        self.spearcross_sound = None
        try:
            indicator_path = os.path.join("Juego", "assets", "Sprites", "warning.png")
            base = pygame.image.load(indicator_path).convert_alpha()
            self.spearcross_indicator = pygame.transform.smoothscale(base, (50, 50))
            print(f"⚠️  Cross indicator sprite cargado: {indicator_path}")
        except Exception:
            print("ℹ️  warning.png no encontrado; usando círculo rojo como fallback")

        try:
            sound_path = os.path.join("Juego", "assets", "Sounds", "crosswarning.wav")
            self.spearcross_sound = pygame.mixer.Sound(sound_path)
            self.spearcross_sound.set_volume(0.6)
            print(f"🔊 Cross warning sound cargado: {sound_path}")
        except Exception:
            print("ℹ️  crosswarning.wav no encontrado; ataque sin sonido de advertencia")

        # Variables para el efecto de titileo
        self.spearcross_flash_timer = 0
        self.spearcross_flash_alpha = 0

    def update_spearcross_flash(self):
        """Actualiza el efecto de titileo del indicador de spearcross."""
        if self.spearcross_flash_timer > 0:
            self.spearcross_flash_timer -= 1
            # Titileo sinusoidal (3 pulsos completos)
            progress = 1.0 - (self.spearcross_flash_timer / 30.0)
            self.spearcross_flash_alpha = int(255 * abs(math.sin(progress * math.pi * 3)))

    def draw_spearcross_flash(self, screen):
        """Dibuja el indicador de titileo en el centro del border."""
        if self.spearcross_flash_timer > 0 and self.spearcross_flash_alpha > 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            center_y = c.BOX_Y + c.BOX_ALTO // 2
            
            if self.spearcross_indicator:
                # Usar sprite con alpha
                indicator = self.spearcross_indicator.copy()
                indicator.set_alpha(self.spearcross_flash_alpha)
                rect = indicator.get_rect(center=(center_x, center_y))
                screen.blit(indicator, rect)
            else:
                # Fallback: círculo rojo pulsante
                surf = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 0, 0, self.spearcross_flash_alpha), (25, 25), 25)
                rect = surf.get_rect(center=(center_x, center_y))
                screen.blit(surf, rect)

    def _apply_simple_sprite(self, b: Bullet):
        """Aplica sprite simplebullet 10x10 si existe, conservando el centro."""
        if self.simplebullet10 is not None:
            center = b.rect.center
            b.image = self.simplebullet10.copy()
            b.rect = b.image.get_rect(center=center)

    def spawn(self, bullet):
        """Safely add bullet to relevant sprite groups."""
        try:
            self.bullets_group.add(bullet)
            if self.all_sprites:
                self.all_sprites.add(bullet)
        except Exception:
            pass

    def clear_attacks(self):
        """Remove all bullets (for phase transitions etc)."""
        try:
            for b in list(self.bullets_group):
                try:
                    b.kill()
                except Exception:
                    pass
        except Exception:
            pass

    def move_diagonal(self, b):
        """Helper for vector movement - uses sub-pixel position if available."""
        sx = float(getattr(b, "speed_x", 0))
        sy = float(getattr(b, "speed_y", 0))
        if hasattr(b, "fx") and hasattr(b, "fy"):
            b.fx += sx
            b.fy += sy
            b.rect.center = (int(b.fx), int(b.fy))
        else:
            b.rect.x += int(round(sx))
            b.rect.y += int(round(sy))
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
                b.rect.left > c.ANCHO or b.rect.right < 0):
            b.kill()

    def move_spiral(self, b, dx, dy):
        """Helper for directional movement - uses sub-pixel floats."""
        if hasattr(b, "fx") and hasattr(b, "fy"):
            b.fx += float(dx)
            b.fy += float(dy)
            b.rect.center = (int(b.fx), int(b.fy))
        else:
            b.rect.x += int(round(dx))
            b.rect.y += int(round(dy))
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
                b.rect.left > c.ANCHO or b.rect.right < 0):
            b.kill()

    # --- attacks ---
    def attack_tutorial(self, timer=0, difficulty=1.0):
        if timer % 13 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y - 20, 4)  # Creada 20px arriba del borde
            b.damage = 1
            self._apply_simple_sprite(b)
            self.spawn(b)

    def attack_rain(self, timer=0, difficulty=1.0):
        step = max(1, int(5 / max(0.1, difficulty)))
        if timer % step == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(6 * difficulty)))
            self._apply_simple_sprite(b)
            self.spawn(b)

    def attack_diagonal(self, timer=0, difficulty=1.0):
        step = max(1, int(4 / max(0.1, difficulty)))
        if timer % step == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 0)
            b.speed_x = direction * max(1, int(3 * difficulty))
            b.speed_y = max(1, int(5 * difficulty))
            b.damage = 2
            b.update = lambda b=b: self.move_diagonal(b)
            self._apply_simple_sprite(b)
            self.spawn(b)

    def attack_lateral1(self, timer=0, difficulty=1.0):
        step = max(1, int(13 / max(0.1, difficulty)))
        if timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X
            dx = max(1, int(6 * difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 3
            b.update = lambda b=b: self.move_diagonal(b)
            self._apply_simple_sprite(b)
            self.spawn(b)

    def attack_lateral2(self, timer=0, difficulty=1.0):
        step = max(1, int(13 / max(0.1, difficulty)))
        if timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X + c.BOX_ANCHO
            dx = -max(1, int(6 * difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 3
            b.update = lambda b=b: self.move_diagonal(b)
            self._apply_simple_sprite(b)
            self.spawn(b)

    def attack_burst1(self, timer=0, difficulty=1.0):
        if timer % 20 == 0:
            center_x = c.ANCHO // 2
            center_y = int(self.boss.rect.centery + 20)
            for angle_deg in range(0, 360, 30):
                angle = math.radians(angle_deg)
                dx = math.cos(angle) * max(2, 4 * difficulty / 1.8)
                dy = math.sin(angle) * max(2, 4 * difficulty / 1.8)
                b = Bullet(center_x, center_y, 0)
                b.damage = 3
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self._apply_simple_sprite(b)
                self.spawn(b)

    def attack_burst2(self, timer=0, difficulty=1.0):
        if timer % 25 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            start_angle = -60
            for i in range(5):
                angle = math.radians(start_angle + i * 30)
                dx = math.cos(angle) * max(2, 5 * difficulty / 1.8)
                dy = math.sin(angle) * max(2, 5 * difficulty / 1.8)
                b = Bullet(center_x, c.BOX_Y + 40, 0)
                b.damage = 3
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self._apply_simple_sprite(b)
                self.spawn(b)

    def attack_burst3(self, timer=0, difficulty=1.0):
        if timer % 90 < 15 and timer % 5 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            for dx in [-4, -2, 0, 2, 4]:
                b = Bullet(center_x, c.BOX_Y + 20, max(1, int(6 * difficulty)))
                b.speed_x = int(dx * difficulty)
                b.speed_y = max(1, int(6 * difficulty))
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self._apply_simple_sprite(b)
                self.spawn(b)

    def attack_spiral(self, timer=0, difficulty=1.0):
        if timer % 15 == 0:
            center_x = c.ANCHO // 2
            center_y = c.BOX_Y + 50
            for i in range(0, 360, 45):
                angle = math.radians(i + timer * 5)
                dx = math.cos(angle) * max(2, 4 * difficulty / 1.8)
                dy = math.sin(angle) * max(2, 4 * difficulty / 1.8)
                b = Bullet(center_x, center_y, 0)
                b.damage = 2
                b.update = lambda dx=dx, dy=dy, b=b: self.move_spiral(b, dx, dy)
                self._apply_simple_sprite(b)
                self.spawn(b)

    def attack_spears(self, timer=0, difficulty=1.0):
        step = max(1, int(40 / max(0.1, difficulty)))
        if timer % step == 0:
            orientacion = random.choice(["vertical", "horizontal"])
            if orientacion == "vertical":
                x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                b = Bullet(x, c.BOX_Y - 100, 0)
                # Falls from top to bottom -> use DOWN-oriented sprite
                if self.spear_d80 is not None:
                    b.image = self.spear_d80.copy()
                else:
                    b.image = pygame.Surface((10, 80), pygame.SRCALPHA).convert_alpha()
                    b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                b.speed_y = max(6, int(9 * difficulty))
                b.damage = 5
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)
            else:
                y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                lado = random.choice(["izq", "der"])
                if lado == "izq":
                    x = c.BOX_X - 60
                    dx = max(2, int(10 * difficulty))
                else:
                    x = c.BOX_X + c.BOX_ANCHO + 60
                    dx = -max(2, int(10 * difficulty))
                b = Bullet(x, y, 0)
                # dx > 0: moving right; dx < 0: moving left
                if dx > 0 and self.spear_r80 is not None:
                    b.image = self.spear_r80.copy()
                elif dx < 0 and self.spear_l80 is not None:
                    b.image = self.spear_l80.copy()
                else:
                    b.image = pygame.Surface((80, 10), pygame.SRCALPHA).convert_alpha()
                    b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = dx
                b.speed_y = 0
                b.damage = 5
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)

    def attack_spearstorm(self, timer=0, difficulty=1.0):
        """Tormenta de lanzas lentas: rafagas desde arriba y costados cada 85 ticks."""
        if timer % 85 == 0:  # cada 85 ticks
            cantidad = random.randint(6, 8)  # muchas lanzas en rafaga

            for _ in range(cantidad):
                orientacion = random.choice(["arriba", "izquierda", "derecha"])

                if orientacion == "arriba":
                    # Lanza que cae desde arriba muy despacio
                    x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                    b = Bullet(x, c.BOX_Y - 100, 0)
                    if self.spear_d70 is not None:
                        b.image = self.spear_d70.copy()
                    else:
                        b.image = pygame.Surface((10, 70), pygame.SRCALPHA).convert_alpha()
                        b.image.fill((180, 200, 255, 220))
                    b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                    b.speed_y = random.uniform(0.4, 0.8)  # muy lenta
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)
                
                elif orientacion == "izquierda":
                    # Lanza desde la izquierda
                    y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                    x = c.BOX_X - 60
                    b = Bullet(x, y, 0)
                    if self.spear_r80 is not None:
                        b.image = self.spear_r80.copy()
                    else:
                        b.image = pygame.Surface((80, 10), pygame.SRCALPHA).convert_alpha()
                        b.image.fill((200, 200, 255, 255))
                    b.rect = b.image.get_rect(center=(x, y))
                    b.speed_x = random.uniform(0.5, 1.0)  # muy lenta
                    b.speed_y = 0
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)
                
                else:  # derecha
                    # Lanza desde la derecha
                    y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                    x = c.BOX_X + c.BOX_ANCHO + 60
                    b = Bullet(x, y, 0)
                    if self.spear_l80 is not None:
                        b.image = self.spear_l80.copy()
                    else:
                        b.image = pygame.Surface((80, 10), pygame.SRCALPHA).convert_alpha()
                        b.image.fill((200, 200, 255, 255))
                    b.rect = b.image.get_rect(center=(x, y))
                    b.speed_x = -random.uniform(0.5, 1.0)  # muy lenta
                    b.speed_y = 0
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)

    # =====================
    #  PHASE 3 SPEAR ATTACKS
    # =====================
    def attack_spearain(self, timer=0, difficulty=1.0):
        """Lluvia vertical de lanzas (versión spear del rain de fase 1)."""
        step = max(1, int(14 / max(0.1, difficulty)))  # menos frecuente
        if timer % step == 0:
            x = random.randint(c.BOX_X + 20, c.BOX_X + c.BOX_ANCHO - 20)
            b = Bullet(x, c.BOX_Y - 60, 0)
            # Imagen y orientación: cae hacia abajo
            if self.spear_d80 is not None:
                b.image = self.spear_d80.copy()
            else:
                b.image = pygame.Surface((10, 80), pygame.SRCALPHA)
                b.image.fill((200, 210, 255, 240))
            b.rect = b.image.get_rect(center=(x, c.BOX_Y - 20))
            b.speed_x = 0
            b.speed_y = max(2, int(4 * difficulty))  # más lenta (antes era 9)
            b.damage = 3
            b.update = lambda b=b: self.move_diagonal(b)
            self.spawn(b)

    def attack_diagonalspear(self, timer=0, difficulty=1.0):
        """Ataques diagonales con lanzas (basado en attack_diagonal)."""
        step = max(1, int(5 / max(0.1, difficulty)))
        if timer % step == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 40, c.BOX_X + c.BOX_ANCHO - 40)
            b = Bullet(x, c.BOX_Y - 40, 0)
            # Usamos sprite hacia abajo; con 4 orientaciones no rotamos al ángulo exacto
            if self.spear_d80 is not None:
                b.image = self.spear_d80.copy()
            else:
                b.image = pygame.Surface((10, 80), pygame.SRCALPHA)
                b.image.fill((200, 210, 255, 240))
            b.rect = b.image.get_rect(center=(x, c.BOX_Y - 10))
            b.speed_x = direction * max(2, int(4 * difficulty))
            b.speed_y = max(3, int(7 * difficulty))
            b.damage = 3
            b.update = lambda b=b: self.move_diagonal(b)
            self.spawn(b)

    def attack_spearwaves(self, timer=0, difficulty=1.0):
        """Rondas de 6-8 lanzas que caen juntas desde arriba, por oleadas."""
        wave_period = max(40, int(120 / max(0.25, difficulty)))  # oleadas más espaciadas
        if timer % wave_period == 0:
            count = random.choice([6])
            # Distribuir de forma casi uniforme dentro del border
            spacing = (c.BOX_ANCHO // (count + 1))
            for i in range(1, count + 1):
                x = c.BOX_X + i * spacing
                b = Bullet(x, c.BOX_Y - 60, 0)
                if self.spear_d80 is not None:
                    b.image = self.spear_d80.copy()
                else:
                    b.image = pygame.Surface((10, 80), pygame.SRCALPHA)
                    b.image.fill((210, 220, 255, 240))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 20))
                b.speed_y = max(2, int(4 * difficulty))  # más lenta (antes era 8)
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)

    def attack_epicborderspear(self, timer=0, difficulty=1.0):
        """Ataque épico: forma un marco de spears pegadas a los 4 bordes del box moviéndose hacia adentro.
        Las spears salen de los 4 lados formando un rectángulo/marco completo, sin spears en el medio.
        """
        edge_period = max(15, int(40 / max(0.2, difficulty)))  # oleadas espaciadas
        if timer % edge_period == 0:
            spear_spacing = 30  # separación entre spears para formar marco denso
            
            # TOP: línea horizontal completa de spears cayendo desde arriba
            n_top = (c.BOX_ANCHO // spear_spacing)
            for i in range(n_top):
                x = c.BOX_X + (i * spear_spacing) + (spear_spacing // 2)
                b = Bullet(x, c.BOX_Y - 80, 0)
                if self.spear_d70 is not None:
                    b.image = self.spear_d70.copy()
                else:
                    b.image = pygame.Surface((10, 70), pygame.SRCALPHA)
                    b.image.fill((200, 200, 255, 240))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                b.speed_y = max(1, int(2 * difficulty))
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)

            # BOTTOM: línea horizontal completa de spears subiendo desde abajo
            n_bottom = (c.BOX_ANCHO // spear_spacing)
            for i in range(n_bottom):
                x = c.BOX_X + (i * spear_spacing) + (spear_spacing // 2)
                b = Bullet(x, c.BOX_Y + c.BOX_ALTO + 60, 0)
                if getattr(self, 'spear_u70', None) is not None:
                    b.image = self.spear_u70.copy()
                else:
                    b.image = pygame.Surface((10, 70), pygame.SRCALPHA)
                    b.image.fill((200, 200, 255, 240))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y + c.BOX_ALTO + 20))
                b.speed_y = -max(1, int(2 * difficulty))
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)

            # IZQUIERDA: línea vertical completa de spears viniendo desde la izquierda
            n_left = (c.BOX_ALTO // spear_spacing)
            for i in range(n_left):
                y = c.BOX_Y + (i * spear_spacing) + (spear_spacing // 2)
                x = c.BOX_X - 60
                dx = max(1, int(2 * difficulty))
                b = Bullet(x, y, 0)
                if self.spear_r70 is not None:
                    b.image = self.spear_r70.copy()
                else:
                    b.image = pygame.Surface((70, 10), pygame.SRCALPHA)
                    b.image.fill((200, 200, 255, 240))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = dx
                b.update = lambda b=b: self.move_diagonal(b)
                b.damage = 3
                self.spawn(b)

            # DERECHA: línea vertical completa de spears viniendo desde la derecha
            n_right = (c.BOX_ALTO // spear_spacing)
            for i in range(n_right):
                y = c.BOX_Y + (i * spear_spacing) + (spear_spacing // 2)
                x = c.BOX_X + c.BOX_ANCHO + 60
                dx = -max(1, int(2 * difficulty))
                b = Bullet(x, y, 0)
                if self.spear_l70 is not None:
                    b.image = self.spear_l70.copy()
                else:
                    b.image = pygame.Surface((70, 10), pygame.SRCALPHA)
                    b.image.fill((200, 200, 255, 240))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = dx
                b.update = lambda b=b: self.move_diagonal(b)
                b.damage = 3
                self.spawn(b)

    # =====================
    # ATAQUES CREATIVOS FASE 3
    # =====================
    
    def attack_spearspiral(self, timer=0, difficulty=1.0):
        """Espiral de lanzas que rotan alrededor del centro del box."""
        step = max(3, int(6 / max(0.1, difficulty)))
        if timer % step == 0:
            # Centro del box
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            center_y = c.BOX_Y + c.BOX_ALTO // 2
            
            # Crear 4 lanzas en ángulos diferentes que roten
            num_spears = 4
            for i in range(num_spears):
                angle = (timer * 2 + i * 90) % 360  # Rotación constante
                radius = 200  # Radio desde el centro
                
                # Calcular posición inicial
                rad = math.radians(angle)
                x = center_x + radius * math.cos(rad)
                y = center_y + radius * math.sin(rad)
                
                b = Bullet(int(x), int(y), 0)
                
                # Elegir sprite según ángulo aproximado
                if 45 <= angle < 135:  # Abajo
                    img = self.spear_d70 if self.spear_d70 else None
                elif 135 <= angle < 225:  # Izquierda
                    img = self.spear_l70 if self.spear_l70 else None
                elif 225 <= angle < 315:  # Arriba
                    img = self.spear_u70 if self.spear_u70 else None
                else:  # Derecha
                    img = self.spear_r70 if self.spear_r70 else None
                
                if img:
                    b.image = img.copy()
                else:
                    b.image = pygame.Surface((10, 70), pygame.SRCALPHA)
                    b.image.fill((255, 200, 150, 240))
                
                b.rect = b.image.get_rect(center=(int(x), int(y)))
                
                # Velocidad hacia el centro
                dx = (center_x - x) / 60
                dy = (center_y - y) / 60
                b.speed_x = dx * max(1.5, difficulty)
                b.speed_y = dy * max(1.5, difficulty)
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self.spawn(b)
    
    def attack_spearx(self, timer=0, difficulty=1.0):
        """Lanzas que forman una X gigante convergiendo al centro."""
        if timer % max(45, int(80 / max(0.3, difficulty))) == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            center_y = c.BOX_Y + c.BOX_ALTO // 2
            
            # Crear 2 diagonales (X)
            num_per_line = 8
            for i in range(num_per_line):
                # Diagonal \ (de arriba-izq a abajo-der)
                progress = i / num_per_line
                x1 = c.BOX_X + progress * c.BOX_ANCHO
                y1 = c.BOX_Y - 60
                
                b1 = Bullet(int(x1), int(y1), 0)
                if self.spear_d80:
                    b1.image = self.spear_d80.copy()
                else:
                    b1.image = pygame.Surface((10, 80), pygame.SRCALPHA)
                    b1.image.fill((200, 150, 255, 240))
                b1.rect = b1.image.get_rect(center=(int(x1), int(y1)))
                b1.speed_x = max(1, int(2 * difficulty))
                b1.speed_y = max(2, int(4 * difficulty))
                b1.damage = 3
                b1.update = lambda b=b1: self.move_diagonal(b)
                self.spawn(b1)
                
                # Diagonal / (de arriba-der a abajo-izq)
                x2 = c.BOX_X + c.BOX_ANCHO - progress * c.BOX_ANCHO
                y2 = c.BOX_Y - 60
                
                b2 = Bullet(int(x2), int(y2), 0)
                if self.spear_d80:
                    b2.image = self.spear_d80.copy()
                else:
                    b2.image = pygame.Surface((10, 80), pygame.SRCALPHA)
                    b2.image.fill((200, 150, 255, 240))
                b2.rect = b2.image.get_rect(center=(int(x2), int(y2)))
                b2.speed_x = -max(1, int(2 * difficulty))
                b2.speed_y = max(2, int(4 * difficulty))
                b2.damage = 3
                b2.update = lambda b=b2: self.move_diagonal(b)
                self.spawn(b2)
    
    def attack_spearcross(self, timer=0, difficulty=1.0):
        """Cruz de lanzas que se expande desde el centro y luego converge.
        Regla: el warning SOLO aparece para el ciclo que sale del centro (expanding)
        y exactamente ~0.5s antes del spawn. Se ajusta si el período es menor a 30.
        """
        period = max(50, int(100 / max(0.3, difficulty)))
        desired_warning = 30  # ~0.5s a 60 FPS
        warning_time = max(1, min(desired_warning, period - 1))  # clamp

        cycle_position = timer % period

        # Determinar ciclo del PRÓXIMO spawn (cuando cycle_position llegue a 0)
        next_cycle_number = ((timer + (period - cycle_position)) // period) % 2
        
        # Disparar advertencia EXACTAMENTE warning_time antes del spawn del próximo ciclo
        # y SOLO si ese ciclo será de expansión (desde el centro).
        if period > warning_time and cycle_position == (period - warning_time) and next_cycle_number == 0:
            self.spearcross_flash_timer = warning_time
            self.spearcross_flash_alpha = 255
            if self.spearcross_sound:
                try:
                    self.spearcross_sound.play()
                except Exception:
                    pass

        # Spawner las spears en el momento exacto
        if timer % period == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            center_y = c.BOX_Y + c.BOX_ALTO // 2
            
            # Alternar entre expandir (ciclo par) y contraer (ciclo impar)
            cycle_number = (timer // period) % 2
            expanding = cycle_number == 0
            
            num_spears = 6
            for direction in ['up', 'down', 'left', 'right']:
                for i in range(num_spears):
                    if expanding:
                        # Spears salen del centro
                        x, y = center_x, center_y
                        if direction == 'up':
                            img = self.spear_u70
                            dx, dy = 0, -max(2, int(3 * difficulty))
                        elif direction == 'down':
                            img = self.spear_d70
                            dx, dy = 0, max(2, int(3 * difficulty))
                        elif direction == 'left':
                            img = self.spear_l70
                            dx, dy = -max(2, int(3 * difficulty)), 0
                        else:  # right
                            img = self.spear_r70
                            dx, dy = max(2, int(3 * difficulty)), 0
                    else:
                        # Spears vienen hacia el centro
                        if direction == 'up':
                            x = center_x
                            y = c.BOX_Y + c.BOX_ALTO + 60
                            img = self.spear_u70
                            dx, dy = 0, -max(2, int(3 * difficulty))
                        elif direction == 'down':
                            x = center_x
                            y = c.BOX_Y - 60
                            img = self.spear_d70
                            dx, dy = 0, max(2, int(3 * difficulty))
                        elif direction == 'left':
                            x = c.BOX_X + c.BOX_ANCHO + 60
                            y = center_y
                            img = self.spear_l70
                            dx, dy = -max(2, int(3 * difficulty)), 0
                        else:  # right
                            x = c.BOX_X - 60
                            y = center_y
                            img = self.spear_r70
                            dx, dy = max(2, int(3 * difficulty)), 0
                    
                    b = Bullet(int(x), int(y), 0)
                    if img:
                        b.image = img.copy()
                    else:
                        size = (70, 10) if direction in ['left', 'right'] else (10, 70)
                        b.image = pygame.Surface(size, pygame.SRCALPHA)
                        b.image.fill((255, 220, 100, 240))
                    b.rect = b.image.get_rect(center=(int(x), int(y)))
                    b.speed_x = dx
                    b.speed_y = dy
                    b.damage = 3
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)
    
    def attack_ballscircle(self, timer=0, difficulty=1.0):
        """Círculo de bolas grandes: aparecen fuera del BOX, entran y luego orbitan."""
        step = max(20, int(40 / max(0.3, difficulty)))
        if timer % step == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            center_y = c.BOX_Y + c.BOX_ALTO // 2

            # Cachear sprite una sola vez si existe
            if self.ballcircle50 is None:
                try:
                    ball_sprite = pygame.image.load("Juego/assets/Sprites/ballcircle.png").convert_alpha()
                    self.ballcircle50 = pygame.transform.smoothscale(ball_sprite, (20, 20))
                    print("🔵 ballcircle.png cargado (50x50)")
                except Exception:
                    self.ballcircle50 = None  # se usará fallback dibujado
                    print("ℹ️  ballcircle.png no encontrado, usando círculo dibujado 50x50")

            # Configuración del patrón
            num_balls = 2
            radius = 150
            angular_speed = 0.03 + 0.01 * max(0.3, difficulty)  # radianes por tick
            approach_speed = 3.0  # velocidad para entrar desde fuera

            for i in range(num_balls):
                angle_deg = (i / num_balls) * 360 + (timer * 2) % 360  # ángulo objetivo sobre el anillo
                rad = math.radians(angle_deg)

                # Posición objetivo sobre el anillo
                target_x = center_x + radius * math.cos(rad)
                target_y = center_y + radius * math.sin(rad)

                # Determinar un punto de spawn FUERA del BOX en la dirección del ángulo
                ux = math.cos(rad)
                uy = math.sin(rad)

                # Elegir borde según componente dominante para garantizar spawn fuera
                if abs(ux) >= abs(uy):
                    # Domina X -> izquierda/derecha
                    if ux > 0:
                        spawn_x = c.BOX_X + c.BOX_ANCHO + 60
                    else:
                        spawn_x = c.BOX_X - 60
                    # Evitar división por cero
                    if abs(ux) < 1e-5:
                        spawn_y = center_y
                    else:
                        spawn_y = center_y + (spawn_x - center_x) * (uy / ux)
                else:
                    # Domina Y -> arriba/abajo
                    if uy > 0:
                        spawn_y = c.BOX_Y + c.BOX_ALTO + 60
                    else:
                        spawn_y = c.BOX_Y - 60
                    if abs(uy) < 1e-5:
                        spawn_x = center_x
                    else:
                        spawn_x = center_x + (spawn_y - center_y) * (ux / uy)

                b = Bullet(int(spawn_x), int(spawn_y), 0)

                # Asignar imagen (sprite o fallback)
                if self.ballcircle50 is not None:
                    b.image = self.ballcircle50.copy()
                else:
                    b.image = pygame.Surface((50, 50), pygame.SRCALPHA)
                    pygame.draw.circle(b.image, (150, 200, 255, 240), (25, 25), 25)
                b.rect = b.image.get_rect(center=(int(spawn_x), int(spawn_y)))

                # Guardar estado para update personalizado
                b.mode = "approach"
                b.target_x = target_x
                b.target_y = target_y
                b.center_x = center_x
                b.center_y = center_y
                b.angle = rad  # ángulo actual sobre la órbita cuando llegue
                b.radius = radius
                b.angular_speed = angular_speed
                b.approach_speed = approach_speed
                b.orbit_ticks = 0
                b.orbit_duration = 90  # ticks en órbita antes de salir
                b.exit_speed = 3.5

                def update_ball(ball=b):
                    # Si está fuera de pantalla por mucho, eliminar
                    if (ball.rect.top > c.ALTO + 200 or ball.rect.bottom < -200 or
                        ball.rect.left > c.ANCHO + 200 or ball.rect.right < -200):
                        try:
                            ball.kill()
                        except Exception:
                            pass
                        return

                    if getattr(ball, 'mode', 'approach') == 'approach':
                        vx = ball.target_x - ball.rect.centerx
                        vy = ball.target_y - ball.rect.centery
                        dist = math.hypot(vx, vy)
                        if dist <= 6:
                            # Acoplado al anillo -> empezar a orbitar
                            ball.mode = 'orbit'
                            ball.rect.center = (int(ball.target_x), int(ball.target_y))
                        else:
                            if dist > 0:
                                ux = vx / dist
                                uy = vy / dist
                                speed = getattr(ball, 'approach_speed', 3.0)
                                ball.rect.x += int(ux * speed)
                                ball.rect.y += int(uy * speed)
                    elif getattr(ball, 'mode') == 'orbit':
                        # Movimiento orbital durante un tiempo limitado
                        ball.angle += getattr(ball, 'angular_speed', 0.03)
                        x = ball.center_x + ball.radius * math.cos(ball.angle)
                        y = ball.center_y + ball.radius * math.sin(ball.angle)
                        ball.rect.center = (int(x), int(y))
                        ball.orbit_ticks = getattr(ball, 'orbit_ticks', 0) + 1
                        # Tras cierto tiempo, pasar a salida
                        if ball.orbit_ticks >= getattr(ball, 'orbit_duration', 90):
                            ball.mode = 'exit'
                            # Vector radial hacia afuera
                            ball.exit_ux = math.cos(ball.angle)
                            ball.exit_uy = math.sin(ball.angle)
                    else:
                        # Salida radial hacia afuera hasta salir de pantalla
                        es = getattr(ball, 'exit_speed', 3.5)
                        ball.rect.x += int(getattr(ball, 'exit_ux', 0) * es)
                        ball.rect.y += int(getattr(ball, 'exit_uy', 0) * es)

                b.update = update_ball
                b.damage = 4
                self.spawn(b)
                

                


                
