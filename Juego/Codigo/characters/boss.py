import pygame, random, math
import Const as c
from characters.bullet import Bullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, bullets_group, all_sprites):
        super().__init__() 
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites
        self.timer = 0
        self.hp = 200

        # --- VISUAL DEL BOSS (👈 NUEVO) ---
        self.image = pygame.image.load("Juego/assets/sprites/Boss_Virus_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))  # ajustá tamaño a gusto
        self.rect = self.image.get_rect(center=(c.ANCHO // 2, 140))
        

                # 💬 Sistema de diálogo
        self.dialogo = None
        self.dialogo_timer = 0
        self.font = pygame.font.Font(None, 28)

        # --- FASES Y ATAQUES ---
        self.phase = 1                 # 👈 Fase actual (1 = virus)
        self.current_attack = "rain"   # 👈 Ataque actual
        self.music_playing = False     # 👈 Para saber si ya sonó la música


        # --------------------------------------------
        #              UPDATE
        # --------------------------------------------

    def update(self):
        self.timer += 1
        keys = pygame.key.get_pressed()

        # --- cambiar ataque manualmente (para probar) ---
        if keys[pygame.K_1]: self.current_attack = "rain"
        if keys[pygame.K_2]: self.current_attack = "diagonal"
        if keys[pygame.K_3]: self.current_attack = "burst"
        if keys[pygame.K_4]: self.current_attack = "spiral"

        # --- Control de FASES ---
        if self.phase == 1:
            self.play_music("assets/music_phase1.mp3")   # 🎵 música de fase 1
            self.phase_one_behavior()

            # 💬 Frases fase 1
            if self.timer == 60:
                self.decir("JAJA, ¿eso es todo lo que tenés?")
            if self.hp < 150 and not hasattr(self, "fase1_dialogo1"):
                self.decir("¡Ni siquiera estás en mi segunda fase!")
                self.fase1_dialogo1 = True

            # Cambia de fase
            if self.hp <= 100:
                self.phase = 2
                self.music_playing = False
                self.image.fill((80, 200, 255))  # 🔵 cambia color (virus → troyano)
                self.decir("¡TE MOSTRARÉ MI VERDADERA FORMA!")  # 😈 diálogo de transición

        elif self.phase == 2:
            self.play_music("assets/music_phase2.mp3")   # 🎵 música de fase 2
            self.phase_two_behavior()

            # 💬 Frases fase 2
            if self.timer % 600 == 0:
                self.decir("¡NO PODÉS DERROTAR A UN TROJANO CHAD!")

        # --- Control del tiempo del diálogo ---
        if self.dialogo_timer > 0:
            self.dialogo_timer -= 1
            if self.dialogo_timer <= 0:
                self.dialogo = None



        # --------------------------------------------
        #             🎮 COMPORTAMIENTOS
        # --------------------------------------------
    def phase_one_behavior(self):
        """Virus: lluvia y diagonales"""
        if self.current_attack == "rain":
            self.attack_rain()
        elif self.current_attack == "diagonal":
            self.attack_diagonal()
    def phase_two_behavior(self):
        """Troyano: más agresivo"""
        if self.current_attack == "burst":
            self.attack_burst()
        elif self.current_attack == "spiral":
            self.attack_spiral()
    # --------------------------------------------
    #             🎵 MÚSICA POR FASE
    # --------------------------------------------
    def play_music(self, filepath):
        if not self.music_playing:
            try:
                pygame.mixer.music.load(r"Juego/assets/Soundtrack/phase1.mp3")
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
                self.music_playing = True
            except Exception as e:
                print("⚠️ Error al reproducir música:", e)
    # --------------------------------------------
    #             💥 ATAQUES
    # --------------------------------------------
    def attack_Tutorial(self):
        if self.timer % 13 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 6)
            self.bullets_group.add(b)
            self.all_sprites.add(b)


    def attack_rain(self):
        if self.timer % 5 == 0:
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 6)
            self.bullets_group.add(b)
            self.all_sprites.add(b)



    def attack_diagonal(self):
        if self.timer % 3 == 0:
            direction = random.choice([-1, 1])
            x = random.randint(c.BOX_X + 10, c.BOX_X + c.BOX_ANCHO - 10)
            b = Bullet(x, c.BOX_Y, 5)
            b.speed_x = direction * 3
            b.speed_y = 5
            b.update = lambda: self.move_diagonal(b)
            self.bullets_group.add(b)
            self.all_sprites.add(b)
    def attack_burst(self):
        if self.timer % 7 == 0:
            center_x = c.BOX_X + c.BOX_ANCHO // 2
            for dx in [-4, -2, 0, 2, 4]:
                b = Bullet(center_x, c.BOX_Y + 20, 5)
                b.speed_x = dx
                b.speed_y = 5
                b.update = lambda: self.move_diagonal(b)
                self.bullets_group.add(b)
                self.all_sprites.add(b)
    def attack_spiral(self):
        if self.timer % 3 == 0:
            center_x = c.ANCHO // 2
            center_y = c.BOX_Y + 50
            for i in range(0, 360, 45):
                angle = math.radians(i + self.timer * 5)
                dx = math.cos(angle) * 4
                dy = math.sin(angle) * 4
                b = Bullet(center_x, center_y, 0)
                b.update = lambda dx=dx, dy=dy, b=b: self.move_spiral(b, dx, dy)
                self.bullets_group.add(b)
                self.all_sprites.add(b)
    # --------------------------------------------
    #            🚀 MOVIMIENTOS EXTRA
    # --------------------------------------------
    def move_diagonal(self, b):
        b.rect.y += b.speed_y
        b.rect.x += b.speed_x
        if b.rect.top > c.ALTO or b.rect.right < 0 or b.rect.left > c.ANCHO:
            b.kill()
    def move_spiral(self, b, dx, dy):
        b.rect.x += dx
        b.rect.y += dy
        if b.rect.top > c.ALTO or b.rect.bottom < 0 or b.rect.right < 0 or b.rect.left > c.ANCHO:
            b.kill()
    # --------------------------------------------
    #            🚀 CHARLITA
    # --------------------------------------------
    def decir(self, texto, duracion=120):
        """Muestra un texto sobre el boss durante cierto tiempo"""
        self.dialogo = texto
        self.dialogo_timer = duracion

    def draw_dialogue(self, screen):
        """Dibuja el diálogo sobre el boss"""
        if self.dialogo:
            render = self.font.render(self.dialogo, True, c.BLANCO)
            rect = render.get_rect(center=(c.ANCHO // 2, 80))
            screen.blit(render, rect)
