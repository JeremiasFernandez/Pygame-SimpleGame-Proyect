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
            self.spawn(b)

    def attack_rain(self, timer=0, difficulty=1.0):
        step = max(1, int(5 / max(0.1, difficulty)))
        if timer % step == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(6 * difficulty)))
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
                    if dx > 0 and self.spear_r70 is not None:
                        b.image = self.spear_r70.copy()
                    elif dx < 0 and self.spear_l70 is not None:
                        b.image = self.spear_l70.copy()
                    else:
                        b.image = pygame.Surface((70, 10), pygame.SRCALPHA).convert_alpha()
                        b.image.fill((180, 200, 255, 220))
                    b.rect = b.image.get_rect(center=(x, y))
                    b.speed_x = dx
                    b.damage = 4
                    b.update = lambda b=b: self.move_diagonal(b)
                    self.spawn(b)
