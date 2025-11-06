import os
import pygame
import Const as c
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class MainMenu:
    def __init__(self):
        self.options = ["Jugar", "Practicar", "Opciones", "Créditos"]
        self.index = 0
        self.next_state = None  # 'play_select' | 'practice' | 'options' | 'credits'
        self.title_font = pygame.font.Font(None, 80)
        self.opt_font = pygame.font.Font(None, 44)
        self.version_font = pygame.font.Font(None, 24)
        
        # Fondo GIF animado
        self.bg_frames = []
        self.bg_frame_index = 0
        self.bg_frame_timer = 0
        self.bg_frame_delay = 50  # ms entre frames
        self._load_background_gif()
        
        # Sonidos
        self.sfx_move = None
        self.sfx_select = None
        try:
            move_path = os.path.join("Juego", "assets", "Sounds", "menu_move.wav")
            self.sfx_move = pygame.mixer.Sound(move_path)
            self.sfx_move.set_volume(0.1)
        except Exception:
            self.sfx_move = None
        try:
            sel_path = os.path.join("Juego", "assets", "Sounds", "menu_select.wav")
            self.sfx_select = pygame.mixer.Sound(sel_path)
            self.sfx_select.set_volume(0.1)
        except Exception:
            self.sfx_select = None

    def _load_background_gif(self):
        """Carga los frames del GIF de fondo"""
        if not PIL_AVAILABLE:
            return
        
        try:
            gif_path = os.path.join("Juego", "assets", "Sprites", "menu_background.gif")
            pil_image = Image.open(gif_path)
            
            # Extraer todos los frames
            frame_count = 0
            while True:
                try:
                    pil_image.seek(frame_count)
                    # Convertir a RGB si es necesario
                    frame = pil_image.convert("RGBA")
                    # Escalar al tamaño de la pantalla
                    frame = frame.resize((c.ANCHO, c.ALTO), Image.Resampling.LANCZOS)
                    # Convertir a superficie de Pygame
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    py_image = pygame.image.fromstring(data, size, mode)
                    self.bg_frames.append(py_image)
                    frame_count += 1
                except EOFError:
                    break
            
            # Obtener el delay del GIF si está disponible
            try:
                pil_image.seek(0)
                duration = pil_image.info.get('duration', 50)
                self.bg_frame_delay = duration
            except Exception:
                pass
                
        except Exception as e:
            print(f"No se pudo cargar menu_background.gif: {e}")
            self.bg_frames = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.index = (self.index - 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.index = (self.index + 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_x):
                if self.sfx_select: self.sfx_select.play()
                # Usar índice para evitar problemas de acentos/strings
                if self.index == 0:      # Jugar
                    self.next_state = "play_select"
                elif self.index == 1:    # Practicar
                    self.next_state = "practice"
                elif self.index == 2:    # Opciones
                    self.next_state = "options"
                elif self.index == 3:    # Créditos
                    self.next_state = "credits"

    def update(self):
        """Actualiza la animación del fondo"""
        if self.bg_frames:
            self.bg_frame_timer += 16.67  # Asumiendo ~60 FPS
            if self.bg_frame_timer >= self.bg_frame_delay:
                self.bg_frame_timer = 0
                self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)

    def draw(self, screen):
        # Dibujar fondo GIF animado
        if self.bg_frames:
            screen.blit(self.bg_frames[self.bg_frame_index], (0, 0))
        else:
            # Fallback si no hay GIF
            screen.fill((20, 20, 35))

        title = self.title_font.render("Bossfight: El troyano", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 120)))

        base_y = 240
        gap = 56
        for i, txt in enumerate(self.options):
            selected = (i == self.index)
            color = (255, 255, 255) if selected else (200, 200, 200)
            surf = self.opt_font.render(txt, True, color)
            rect = surf.get_rect(center=(c.ANCHO // 2, base_y + i * gap))
            if selected:
                # simple selector >>
                arrow = self.opt_font.render(">", True, (85, 171, 77))
                screen.blit(arrow, (rect.left - 40, rect.top))
            screen.blit(surf, rect)

        # Etiqueta de versión (abajo a la derecha, semitransparente)
        ver_text = "v0.7.0 (Pre-alpha)"
        ver_surf = self.version_font.render(ver_text, True, (220, 220, 230))
        ver_surf.set_alpha(140)
        vx = c.ANCHO - ver_surf.get_width() - 12
        vy = c.ALTO - ver_surf.get_height() - 10
        screen.blit(ver_surf, (vx, vy))
