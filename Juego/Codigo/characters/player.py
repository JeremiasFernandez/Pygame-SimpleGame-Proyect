"""
player.py - Clase del Jugador
==============================
Define el comportamiento del personaje controlado por el jugador,
incluyendo movimiento, animaciones, daño e invencibilidad.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pygame
import Const as c


# ============================================================================
# SISTEMA DE CHEAT CODES
# ============================================================================
_cheat_buffer = ""


def process_menu_cheat_key(key) -> bool:
    """
    Detecta el código de cheat 'UTNFRA' en el menú principal.
    
    Args:
        key: Tecla presionada (pygame.K_*)
        
    Returns:
        True si se completó el código, False en caso contrario.
    """
    global _cheat_buffer
    
    # Solo procesar letras A-Z
    if pygame.K_a <= key <= pygame.K_z:
        ch = chr(key - pygame.K_a + ord('A'))
        _cheat_buffer = (_cheat_buffer + ch)[-6:]  # Mantener últimos 6 caracteres
        return _cheat_buffer == "UTNFRA"
    return False


def reset_menu_cheat():
    """Reinicia el buffer del código de cheat."""
    global _cheat_buffer
    _cheat_buffer = ""


# ============================================================================
# CLASE PLAYER
# ============================================================================
class Player(pygame.sprite.Sprite):
    """
    Representa al jugador controlable durante el combate.
    Maneja movimiento, colisiones, daño, invencibilidad y animaciones.
    """
    
    def __init__(self):
        super().__init__()
        
        # Cargar sprites
        self._load_sprites()
        
        # Configurar sprite y hitbox iniciales
        self.image = self.image_normal
        self.rect = self.image.get_rect(center=(c.ANCHO // 2, c.ALTO - 100))
        self.rect.inflate_ip(-18, -18)  # Reducir hitbox para colisiones más justas
        
        self.hitbox = pygame.Rect(0, 0, 10, 10)
        self.hitbox.center = self.rect.center
        
        # Cargar sonidos
        self._load_sounds()
        
        # Propiedades del jugador
        self.vel = 3
        self.hp = 20
        self.invencible = False
        self.tiempo_inv = 0
        self.parpadeo_timer = 0
        self.x_pressed = False
    
    def _load_sprites(self):
        """Carga y escala todos los sprites del jugador."""
        try:
            self.image_normal = pygame.image.load("Juego/assets/sprites/player1.png").convert_alpha()
            self.image_damaged = pygame.image.load("Juego/assets/sprites/player_damaged.png").convert_alpha()
            self.image_x = pygame.image.load("Juego/assets/sprites/player_x.png").convert_alpha()
            
            # Escalar a 32x32
            self.image_normal = pygame.transform.scale(self.image_normal, (32, 32))
            self.image_damaged = pygame.transform.scale(self.image_damaged, (32, 32))
            self.image_x = pygame.transform.scale(self.image_x, (32, 32))
        except Exception as e:
            print(f"⚠️ Error cargando sprites del jugador: {e}")
            # Crear sprites de fallback
            self.image_normal = pygame.Surface((32, 32))
            self.image_normal.fill((100, 100, 255))
            self.image_damaged = self.image_normal.copy()
            self.image_x = self.image_normal.copy()
    
    def _load_sounds(self):
        """Carga los efectos de sonido del jugador."""
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
    
    def update(self, keys):
        """
        Actualiza el estado del jugador cada frame.
        
        Args:
            keys: Estado de las teclas (pygame.key.get_pressed())
        """
        self._handle_movement(keys)
        self._handle_invincibility()
        self._handle_x_sprite(keys)
    
    def _handle_movement(self, keys):
        """Maneja el movimiento del jugador con límites del área de combate."""
        # Movimiento en 4 direcciones
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.vel
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.vel
        
        # Restringir movimiento al área de combate
        if self.rect.left < c.BOX_X:
            self.rect.left = c.BOX_X
        if self.rect.right > c.BOX_X + c.BOX_ANCHO:
            self.rect.right = c.BOX_X + c.BOX_ANCHO
        if self.rect.top < c.BOX_Y:
            self.rect.top = c.BOX_Y
        if self.rect.bottom > c.BOX_Y + c.BOX_ALTO:
            self.rect.bottom = c.BOX_Y + c.BOX_ALTO
    
    def _handle_invincibility(self):
        """Maneja los frames de invencibilidad y el parpadeo visual."""
        if self.invencible:
            self.tiempo_inv -= 1
            self.parpadeo_timer += 1
            
            # Parpadeo cada 4 frames
            if self.parpadeo_timer % 4 == 0:
                alpha_actual = self.image.get_alpha()
                if alpha_actual is None or alpha_actual == 255:
                    self.image.set_alpha(60)
                else:
                    self.image.set_alpha(255)
            
            # Terminar invencibilidad
            if self.tiempo_inv <= 0:
                self.invencible = False
                self.image = self.image_normal
                self.image.set_alpha(255)
    
    def _handle_x_sprite(self, keys):
        """Maneja el cambio de sprite al presionar X o Numpad 0."""
        trigger_pressed = keys[pygame.K_x] or keys[pygame.K_KP0]
        
        if trigger_pressed:
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
        """
        Aplica daño al jugador si no está invencible.
        
        Args:
            amount: Cantidad de daño a recibir.
        """
        if not self.invencible:
            self.hp -= amount
            self.invencible = True
            self.tiempo_inv = int(0.6 * c.FPS)  # 0.6 segundos de invencibilidad
            self.image = self.image_damaged
            self.parpadeo_timer = 0
            
            print(f"Daño recibido: -{amount} HP ({self.hp} restantes)")
            
            if self.damage_sound:
                self.damage_sound.play()
    
    def draw_health_bar(self, screen):
        """
        Dibuja la barra de vida del jugador en la pantalla.
        
        Args:
            screen: Superficie de Pygame donde dibujar.
        """
        vida_max = 20
        vida_actual = max(0, self.hp)
        
        # Configuración de la barra
        barra_x, barra_y = 20, 20
        barra_ancho, barra_alto = 200, 20
        
        # Calcular proporción de vida
        proporcion = vida_actual / vida_max
        ancho_relleno = int(barra_ancho * proporcion)
        
        # Dibujar barra
        pygame.draw.rect(screen, c.GRIS, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, (0, 255, 0), (barra_x, barra_y, ancho_relleno, barra_alto))
        pygame.draw.rect(screen, c.BLANCO, (barra_x, barra_y, barra_ancho, barra_alto), 2)
