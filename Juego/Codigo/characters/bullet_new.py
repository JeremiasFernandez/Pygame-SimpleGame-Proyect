# characters/bullet.py
import pygame
import random
import math
import Const as c

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(c.BLANCO)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > c.ALTO:
            self.kill()

class AttackManager:
    def __init__(self, boss, bullets_group, all_sprites):
        self.boss = boss
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites

    def spawn(self, bullet):
        """Añade una bala a los grupos de sprites."""
        self.bullets_group.add(bullet)
        if self.all_sprites is not None:
            self.all_sprites.add(bullet)

    def clear_attacks(self):
        """Remove/kill all active bullets and any related effects (best-effort).
        Calling this ensures no lingering sprites remain during phase transitions.
        """
        try:
            for b in list(self.bullets_group):
                try:
                    b.kill()
                except Exception:
                    # ignore individual kill failures
                    pass
        except Exception:
            pass

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
            
    def attack_tutorial(self, timer=0, difficulty=1.0):
        if timer % 13 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 4)
            b.damage = 1
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_rain(self, timer=0, difficulty=1.0):
        step = max(1, int(5 / difficulty))
        if timer % step == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(6 * difficulty)))
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_diagonal(self, timer=0, difficulty=1.0):
        step = max(1, int(4 / difficulty))
        if timer % step == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, max(1, int(5 * difficulty)))
            b.speed_x = direction * max(1, int(3 * difficulty))
            b.speed_y = max(1, int(5 * difficulty))
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_lateral1(self, timer=0, difficulty=1.0):
        step = max(1, int(13 / difficulty))
        if timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X
            dx = max(1, int(6 * difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 2
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_lateral2(self, timer=0, difficulty=1.0):
        step = max(1, int(13 / difficulty))
        if timer % step == 0:
            y = random.randint(c.BOX_Y + 20, c.BOX_Y + c.BOX_ALTO - 50)
            x = c.BOX_X + c.BOX_ANCHO
            dx = -max(1, int(6 * difficulty))
            b = Bullet(x, y, 0)
            b.speed_x = dx
            b.speed_y = 0
            b.damage = 2
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)

    def attack_burst1(self, timer=0, difficulty=1.0):
        if timer % 20 == 0:
            center_x = c.ANCHO // 2
            center_y = self.boss.rect.centery + 20
            for angle_deg in range(0, 360, 30):
                angle = math.radians(angle_deg)
                dx = math.cos(angle) * max(2, 4 * difficulty / 1.8)
                dy = math.sin(angle) * max(2, 4 * difficulty / 1.8)
                b = Bullet(center_x, center_y, 0)
                b.damage = 2
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_burst2(self, timer=0, difficulty=1.0):
        if timer % 25 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            start_angle = -60
            for i in range(5):
                angle = math.radians(start_angle + i * 30)
                dx = math.cos(angle) * max(2, 5 * difficulty / 1.8)
                dy = math.sin(angle) * max(2, 5 * difficulty / 1.8)
                b = Bullet(center_x, c.BOX_Y + 40, 0)
                b.damage = 2
                b.update = lambda b=b, dx=dx, dy=dy: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_burst3(self, timer=0, difficulty=1.0):
        # tres ráfagas cortas seguidas
        if timer % 90 < 15 and timer % 5 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            for dx in [-4, -2, 0, 2, 4]:
                b = Bullet(center_x, c.BOX_Y + 20, max(1, int(6 * difficulty)))
                b.speed_x = int(dx * difficulty)
                b.speed_y = max(1, int(6 * difficulty))
                b.damage = 2
                b.update = lambda b=b: self.move_diagonal(b)
                self.bullets_group.add(b)
                self.all_sprites.add(b)

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
                self.bullets_group.add(b)
                self.all_sprites.add(b)

    def attack_spears(self, timer=0, difficulty=1.0):
        """Lanzas largas verticales u horizontales (más duras en fase 2)."""
        step = max(1, int(40 / difficulty))
        if timer % step == 0:
            orientacion = random.choice(["vertical", "horizontal"])

            if orientacion == "vertical":
                x = random.randint(c.BOX_X + 30, c.BOX_X + c.BOX_ANCHO - 30)
                b = Bullet(x, c.BOX_Y - 100, 0)
                # superficie alargada (convert_alpha para blend)
                b.image = pygame.Surface((10, 80), pygame.SRCALPHA).convert_alpha()
                b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, c.BOX_Y - 30))
                b.speed_y = max(2, int(9 * difficulty))
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)

            else:
                y = random.randint(c.BOX_Y + 40, c.BOX_Y + c.BOX_ALTO - 40)
                lado = random.choice(["izq", "der"])
                if lado == "izq":
                    x = c.BOX_X - 60
                    dx = max(2, int(10 * difficulty))
                else:
                    x = c.BOX_X + c.BOX_ANCHO + 60
                    dx = -max(2, int(10 * difficulty))
                
                # Crear bala horizontal
                b = Bullet(x, y, 0)
                b.image = pygame.Surface((80, 10), pygame.SRCALPHA).convert_alpha()
                b.image.fill((200, 200, 255, 255))
                b.rect = b.image.get_rect(center=(x, y))
                b.speed_x = dx
                b.speed_y = 0
                b.damage = 3
                b.update = lambda b=b: self.move_diagonal(b)
                self.bullets_group.add(b)
                self.all_sprites.add(b)