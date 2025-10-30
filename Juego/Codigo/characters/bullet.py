# characters/bullet.py
import pygame
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
