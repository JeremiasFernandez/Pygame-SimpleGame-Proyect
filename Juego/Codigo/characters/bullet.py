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

    def update(self):
        """Combined default vertical speed + vector movement if set."""
        # Add vertical speed
        self.rect.y += self.speed
        # Add any vector movement 
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Remove if outside screen
        if (self.rect.top > c.ALTO or self.rect.bottom < 0 or
                self.rect.left > c.ANCHO or self.rect.right < 0):
            self.kill()

class AttackManager:
    def __init__(self, boss, bullets_group, all_sprites=None):
        self.boss = boss
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites

        # --- Simple Bullet sprite (for normal bullets) ---
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
        """Helper for vector movement - use speed_x/speed_y."""
        b.rect.x += getattr(b, "speed_x", 0)
        b.rect.y += getattr(b, "speed_y", 0)
        if (b.rect.top > c.ALTO or b.rect.bottom < 0 or
                b.rect.left > c.ANCHO or b.rect.right < 0):
            b.kill()

    def move_spiral(self, b, dx, dy):
        """Helper for directional movement - use dx/dy."""
        b.rect.x += dx
        b.rect.y += dy
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
                b.speed_y = max(2, int(9 * difficulty))
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
        """Tormenta de lanzas lentas: salen muchas constantemente, muy despacio."""
        if timer % 75 == 0:  # cada pocos frames
            cantidad = random.randint(6, 10)  # varias lanzas por tick

            for _ in range(cantidad):
                orientacion = random.choice(["vertical", "horizontal"])

                if orientacion == "vertical":
                    # Lanza que cae desde arriba muy despacio
                    x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                    b = Bullet(x, c.BOX_Y - 100, 0)
                    if self.spear_d70 is not None:
                        b.image = self.spear_d70.copy()
                    else:
                        b.image = pygame.Surface((10, 70), pygame.SRCALPHA).convert_alpha()
                        b.image.fill((180, 200, 255, 220))  # un poco translúcida
                    b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                    b.speed_y = random.uniform(0.5, 1.2)  # super lenta
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)

    # =====================
    #  PHASE 3 SPEAR ATTACKS
    # =====================
    def attack_spearain(self, timer=0, difficulty=1.0):
        """Lluvia vertical de lanzas (versión spear del rain de fase 1)."""
        step = max(1, int(8 / max(0.1, difficulty)))  # menos frecuente
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
            b.damage = 5
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
            b.damage = 6
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
                b.damage = 5
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
                b.damage = 4
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
                b.damage = 4
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
                b.damage = 4
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
                b.damage = 4
                self.spawn(b)
                

                
