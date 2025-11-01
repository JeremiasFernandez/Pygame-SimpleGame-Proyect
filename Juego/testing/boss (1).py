import pygame
import math

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Juego/assets/sprites/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 100

        # Posición base para movimiento flotante
        self.base_pos = self.rect.center

    def update(self):
        self.oscilar()

    def oscilar(self):
        tiempo = pygame.time.get_ticks() / 1000  # tiempo en segundos
        offset_y = math.sin(tiempo * 2) * 5       # oscilación vertical
        offset_x = math.cos(tiempo * 1.5) * 3     # oscilación horizontal
        self.rect.center = (self.base_pos[0] + offset_x, self.base_pos[1] + offset_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
