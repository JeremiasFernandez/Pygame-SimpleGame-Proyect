import pygame
import math
import os

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.phase = 1
        self.image = pygame.image.load(os.path.join("Juego", "assets", "Sprites", "BossVirus.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.base_pos = self.rect.center
        self.hp = 200
        self.max_hp = 200
        self.font = pygame.font.Font(None, 24)
        self.phase = 1
        self.dead_timer = 0
        self.silence_played = False
        self.phase3_started = False

        self.dead_timer = 0
        self.silence_played = False
        self.phase3_started = False

    def update(self):
        self.oscilar()
        if self.hp <= 0 and self.phase == 1:
            # Fase de "muerte"
            if not self.silence_played:
                try:
                    pygame.mixer.music.load(os.path.join("Juego", "assets", "Sounds", "silence.mp3"))
                    pygame.mixer.music.play()
                    self.image = pygame.image.load(os.path.join("Juego", "assets", "Sprites", "boss_derrotado.png")).convert_alpha()
                    print("🔇 Se reproduce silencio...")
                    self.silence_played = True
                    self.dead_timer = pygame.time.get_ticks()
                except Exception as e:
                    print(f"❌ Error al reproducir silencio: {e}")

            # Esperar 5 segundos antes de fase 3
            if self.silence_played and not self.phase3_started:
                if pygame.time.get_ticks() - self.dead_timer >= 5000:
                    self.phase = 3
                    self.hp = 250
                    self.max_hp = 250
                    self.image = pygame.image.load(os.path.join("Juego", "assets", "Sprites", "Boss_Virus_3.png")).convert_alpha()
                    try:
                        pygame.mixer.music.load(os.path.join("Juego", "assets", "Sounds", "phase3.mp3"))
                        pygame.mixer.music.play(-1)
                        print("🎵 Música de fase 3 iniciada")
                    except Exception as e:
                        print(f"❌ Error al cargar música fase 3: {e}")
                    self.phase3_started = True
        # Lógica de transición a fase 3
        if self.hp <= 0 and self.phase == 1:
            if not self.silence_played:
                try:
                    pygame.mixer.music.load(os.path.join("Juego", "assets", "Sounds", "silence.mp3"))
                    pygame.mixer.music.play()
                    self.image = pygame.image.load(os.path.join("Juego", "assets", "Sprites", "boss_derrotado.png")).convert_alpha()
                    print("🔇 Se reproduce silencio...")
                    self.silence_played = True
                    self.dead_timer = pygame.time.get_ticks()
                except Exception as e:
                    print(f"❌ Error al reproducir silencio: {e}")

            if self.silence_played and not self.phase3_started:
                if pygame.time.get_ticks() - self.dead_timer >= 5000:
                    self.phase = 3
                    self.hp = 250
                    self.max_hp = 250
                    self.image = pygame.image.load(os.path.join("Juego", "assets", "Sprites", "Boss_Virus_3.png")).convert_alpha()
                    try:
                        pygame.mixer.music.load(os.path.join("Juego", "assets", "Sounds", "phase3.mp3"))
                        pygame.mixer.music.play(-1)
                        print("🎵 Música de fase 3 iniciada")
                    except Exception as e:
                        print(f"❌ Error al cargar música fase 3: {e}")
                    self.phase3_started = True


    def draw_hp_bar(self, screen):
        bar_width = 200
        bar_height = 20
        x = self.rect.centerx - bar_width // 2
        y = self.rect.top - 30

        fill = int(self.hp / self.max_hp * bar_width)
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

        hp_text = self.font.render(f"{self.hp}/{self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (x + bar_width + 10, y))

    def oscilar(self):
        tiempo = pygame.time.get_ticks() / 1000
        offset_y = math.sin(tiempo * 2) * 5
        offset_x = math.cos(tiempo * 1.5) * 3
        self.rect.center = (self.base_pos[0] + offset_x, self.base_pos[1] + offset_y)
