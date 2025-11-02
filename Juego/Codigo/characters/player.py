import pygame
import Const as c  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # --- Cargar y escalar sprites ---
        self.image_normal = pygame.image.load("Juego/assets/sprites/player1.png").convert_alpha()
        self.image_damaged = pygame.image.load("Juego/assets/sprites/player_damaged.png").convert_alpha()
        self.image_x = pygame.image.load("Juego/assets/sprites/player_x.png").convert_alpha()

        self.image_normal = pygame.transform.scale(self.image_normal, (32, 32))
        self.image_damaged = pygame.transform.scale(self.image_damaged, (32, 32))
        self.image_x = pygame.transform.scale(self.image_x, (32, 32))

        # --- Sprite actual ---
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(c.ANCHO // 2, c.ALTO - 100))
        self.rect.inflate_ip(-18, -18)  # Ajustar tamaño del rectángulo de colisión

        # --- Hitbox ---
        self.hitbox = pygame.Rect(0, 0, 10, 10)
        self.hitbox.center = self.rect.center

        # --- Sonidos ---
        try:
            self.damage_sound = pygame.mixer.Sound("Juego/assets/Sounds/hit.wav")
            self.damage_sound.set_volume(0.4)
        except:
            self.damage_sound = None
            print("⚠️ No se pudo cargar el sonido de daño.")

        try:
            self.sonido_cambio = pygame.mixer.Sound("Juego/assets/Sounds/clicking.wav")
            self.sonido_cambio.set_volume(0.4)
        except:
            self.sonido_cambio = None
            print("⚠️ No se pudo cargar el sonido de click.")

        # --- Propiedades ---
        self.vel = 3
        self.hp = 20
        self.invencible = False
        self.tiempo_inv = 0
        self.parpadeo_timer = 0
        self.x_pressed = False

    def update(self, keys):
        # --- Movimiento ---
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vel
        if keys[pygame.K_UP]:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.rect.y += self.vel

        # --- Límites del cuadro de movimiento ---
        if self.rect.left < c.BOX_X:
            self.rect.left = c.BOX_X
        if self.rect.right > c.BOX_X + c.BOX_ANCHO:
            self.rect.right = c.BOX_X + c.BOX_ANCHO
        if self.rect.top < c.BOX_Y:
            self.rect.top = c.BOX_Y
        if self.rect.bottom > c.BOX_Y + c.BOX_ALTO:
            self.rect.bottom = c.BOX_Y + c.BOX_ALTO

        # --- Invencibilidad y parpadeo ---
        if self.invencible:
            self.tiempo_inv -= 1
            self.parpadeo_timer += 1
            if self.parpadeo_timer % 4 == 0:
                alpha_actual = self.image.get_alpha()
                if alpha_actual is None or alpha_actual == 255:
                    self.image.set_alpha(60)
                else:
                    self.image.set_alpha(255)
            if self.tiempo_inv <= 0:
                self.invencible = False
                self.image = self.image_normal
                self.image.set_alpha(255)

        # --- Sprite al presionar X ---
        if keys[pygame.K_x]:
            if not self.x_pressed:
                self.x_pressed = True
                self.image = self.image_x
                if self.sonido_cambio:
                    self.sonido_cambio.play()
        else:
            if self.x_pressed:
                self.x_pressed = False
            if not self.invencible:
                self.image = self.image_normal

    def take_damage(self, amount):
        if not self.invencible:
            self.hp -= amount
            self.invencible = True
            self.tiempo_inv = int(0.6 * c.FPS)
            self.image = self.image_damaged
            self.parpadeo_timer = 0
            print(f"Daño recibido: -{amount} HP ({self.hp} restantes)")
            if self.damage_sound:
                self.damage_sound.play()

    def draw_health_bar(self, screen):
        vida_max = 20
        vida_actual = self.hp
        barra_x, barra_y = 20, 20
        barra_ancho, barra_alto = 200, 20
        proporcion = max(0, vida_actual / vida_max)
        ancho_relleno = int(barra_ancho * proporcion)

        pygame.draw.rect(screen, c.GRIS, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, (0, 255, 0), (barra_x, barra_y, ancho_relleno, barra_alto))
        pygame.draw.rect(screen, c.BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)
