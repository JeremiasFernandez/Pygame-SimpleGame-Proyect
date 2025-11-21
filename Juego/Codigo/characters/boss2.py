import os, random, math, pygame
import Const as c
from characters.bullet import AttackManager, Bullet

class Boss2(pygame.sprite.Sprite):
    """Boss secreto (requiere 2 estrellas).
    - 200 HP, cambia a fase 2 al llegar a 100.
    - Fase 1: ataques mixtos simples (rain, diagonal, burst1).
    - Fase 2: ataques spear + círculo + bursts más rápidos.
    - Cambia sprite y música al entrar en fase 2.
    """
    def __init__(self, bullets_group, all_sprites, music_volume=0.5):
        super().__init__()
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites
        self.attack_manager = AttackManager(self, bullets_group, all_sprites)
        self.hp = 200
        self.phase = 1
        self.difficulty = 1.0
        self.music_volume = music_volume
        self.current_attack = None
        self.attack_timer = 0
        self.timer = 0

        # Cargar sprites SECRETOS (diferentes al boss original)
        self.image_phase1 = self._load_scaled("Boss_Secret.png", (210,280))
        self.image_phase2 = self._load_scaled("Boss_Secret2.png", (210,280))
        self.image = self.image_phase1
        self.rect = self.image.get_rect(center=(c.ANCHO//2, c.BOX_Y - 120))

        # Pools de ataques ÚNICOS Y ORIGINALES
        # Fase 1: Ataques moderados con patrones visuales únicos
        self.phase1_attacks = [
            "attack_spiral_burst",
            "attack_wave_pattern",
            "attack_rotating_shield",
            "attack_ballscircle",
            "attack_spearwaves"
        ]
        # Fase 2: Ataques más agresivos y complejos
        self.phase2_attacks = [
            "attack_spiral_burst",
            "attack_wave_pattern",
            "attack_rotating_shield",
            "attack_zigzag_laser",
            "attack_cross_explosion",
            "attack_spiral_spears",
            "attack_spiral_burst",
            "attack_ballscircle",
            "attack_spearwaves",
            "attack_spears",
            "attack_spearstorm",
            "attack_spearain",
            "attack_spearwaves",
            "attack_spearcross",
            "attack_ballscircle",
        ]

        # Música SECRETA (phase4 para fase 1)
        self._play_music("phase4.mp3")

    def _load_scaled(self, name, size):
        path = os.path.join("Juego", "assets", "Sprites", name)
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.smoothscale(img, size)
        except Exception:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((140,140,140,255))
            return surf

    def _play_music(self, filename):
        try:
            mpath = os.path.join("Juego", "assets", "Soundtrack", filename)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(mpath)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[WARNING] musica {filename} no cargada: {e}")

    def update(self):
        if self.hp <= 100 and self.phase == 1:
            self._enter_phase2()

        self.timer += 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if not self.current_attack or self.attack_timer <= 0:
            self._choose_attack()
        # Ejecutar ataque
        if self.current_attack:
            try:
                method = getattr(self.attack_manager, self.current_attack)
                method(self.timer, self.difficulty)
            except Exception as e:
                print(f"[WARNING] error ataque {self.current_attack}: {e}")
                self.current_attack = None

    def _choose_attack(self):
        pool = self.phase1_attacks if self.phase == 1 else self.phase2_attacks
        posibles = [a for a in pool if a != self.current_attack] or pool
        self.current_attack = random.choice(posibles)
        self.attack_timer = 120 if self.phase == 1 else 90
        print(f"[BOSS2] Ataque seleccionado: {self.current_attack} (fase {self.phase}, HP={self.hp})")

    def _enter_phase2(self):
        self.phase = 2
        self.difficulty = 1.4
        center = self.rect.center
        self.image = self.image_phase2
        self.rect = self.image.get_rect(center=center)
        self._play_music("phase5.mp3")  # Música SECRETA para fase 2
        self.current_attack = None
        self.attack_timer = 0
        print("[BOSS2] Fase 2 activada con música phase5.mp3")

    def hit(self, damage=10):
        self.hp -= damage
        if self.hp <= 0:
            self._die()

    def _die(self):
        pygame.mixer.music.stop()
        self.current_attack = None
        self.image.fill((50,50,50,220), special_flags=pygame.BLEND_RGBA_MULT)
        print("[BOSS2] Derrotado")

    def draw_health_bar(self, screen):
        vida_max = 200
        vida_actual = max(0, self.hp)
        w, h = 240, 14
        x = c.ANCHO//2 - w//2
        y = 24
        propor = vida_actual / vida_max
        pygame.draw.rect(screen, c.GRIS, (x,y,w,h))
        pygame.draw.rect(screen, (0,180,255) if self.phase==1 else (255,80,60), (x,y,int(w*propor),h))
        pygame.draw.rect(screen, c.BLANCO, (x,y,w,h),2)
        f = pygame.font.Font(None,24)
        t = f.render(f"{vida_actual}/{vida_max}", True, c.BLANCO)
        screen.blit(t, t.get_rect(center=(c.ANCHO//2, y+h//2)))
