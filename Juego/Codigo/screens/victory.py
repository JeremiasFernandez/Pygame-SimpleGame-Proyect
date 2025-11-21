"""
victory.py - Pantalla de Victoria
==================================
Pantalla que se muestra al derrotar al jefe final.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pygame
import os
import Const as c


# ============================================================================
# CLASE VICTORYSCREEN
# ============================================================================
class VictoryScreen:
    """
    Pantalla de victoria con animaciones, estadísticas y opciones.
    """
    
    def __init__(self, difficulty_label: str, intentos: int, is_practice: bool = False):
        """
        Inicializa la pantalla de victoria.
        
        Args:
            difficulty_label: Dificultad jugada ("Junior" o "Senior")
            intentos: Número de intentos totales
            is_practice: Si fue en modo práctica (no otorga estrellas)
        """
        self.difficulty_label = difficulty_label
        self.intentos = intentos
        self.is_practice = is_practice
        
        # Fuentes
        self.title_font = pygame.font.Font(None, 90)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        # Estado de animación
        self.timer = 0
        self.phase = "fade_in"  # fade_in -> text_reveal -> options
        self.fade_alpha = 0
        self.text_reveal_progress = 0
        
        # Opciones
        self.options = ["Volver al Menú", "Salir"]
        self.selected_option = 0
        self.can_select = False  # Se habilita después de las animaciones
        
        # Partículas de celebración
        self.particles = []
        self._create_particles()
        
        # Sonidos
        self._load_sounds()
        
        # Reproducir música de victoria
        self._play_victory_music()
    
    def _load_sounds(self):
        """Carga los efectos de sonido."""
        try:
            self.victory_sound = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "epic.wav"))
            self.victory_sound.set_volume(0.6)
        except Exception:
            self.victory_sound = None
            print("[WARNING] No se pudo cargar sonido de victoria")
        
        try:
            self.menu_move = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "menu_move.wav"))
            self.menu_move.set_volume(0.1)
        except Exception:
            self.menu_move = None
        
        try:
            self.menu_select = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "menu_select.wav"))
            self.menu_select.set_volume(0.1)
        except Exception:
            self.menu_select = None
    
    def _play_victory_music(self):
        """Reproduce la música de victoria."""
        try:
            pygame.mixer.music.stop()
            # Intentar cargar música de victoria
            victory_music_paths = [
                "Juego/assets/Soundtrack/VictoryTheme.mp3",  # preferido si existe
                "Juego/assets/Soundtrack/victory.mp3",
                "Juego/assets/Soundtrack/menu_theme_complete.mp3",
            ]
            
            for path in victory_music_paths:
                try:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print(f"[MUSIC] Musica de victoria: {path}")
                    break
                except Exception:
                    continue
            
            # Reproducir sonido de victoria una vez
            if self.victory_sound:
                self.victory_sound.play()
        
        except Exception as e:
            print(f"[WARNING] Error reproduciendo música de victoria: {e}")
    
    def _create_particles(self):
        """Crea partículas de celebración."""
        import random
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, c.ANCHO),
                'y': random.randint(-100, c.ALTO),
                'speed_y': random.uniform(1, 3),
                'speed_x': random.uniform(-0.5, 0.5),
                'color': random.choice([
                    (255, 215, 0),   # Dorado
                    (255, 255, 100), # Amarillo brillante
                    (255, 200, 255), # Rosa claro
                    (200, 200, 255), # Azul claro
                ]),
                'size': random.randint(3, 7)
            })
    
    def handle_event(self, event):
        """
        Maneja eventos de teclado.
        
        Returns:
            'menu' si se selecciona volver al menú
            'quit' si se selecciona salir
            None en caso contrario
        """
        if not self.can_select:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_option = (self.selected_option - 1) % len(self.options)
                if self.menu_move:
                    self.menu_move.play()
            
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_option = (self.selected_option + 1) % len(self.options)
                if self.menu_move:
                    self.menu_move.play()
            
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_x):
                if self.menu_select:
                    self.menu_select.play()
                
                if self.selected_option == 0:
                    return 'menu'
                else:
                    return 'quit'
        
        return None
    
    def update(self):
        """Actualiza la animación de la pantalla."""
        self.timer += 1
        
        # Fase de fade in (0-60 frames)
        if self.phase == "fade_in":
            self.fade_alpha = min(255, (self.timer / 60) * 255)
            if self.timer >= 60:
                self.phase = "text_reveal"
                self.timer = 0
        
        # Fase de revelación de texto (60-120 frames)
        elif self.phase == "text_reveal":
            self.text_reveal_progress = min(1.0, self.timer / 60)
            if self.timer >= 60:
                self.phase = "options"
                self.can_select = True
                self.timer = 0
        
        # Actualizar partículas
        for particle in self.particles:
            particle['y'] += particle['speed_y']
            particle['x'] += particle['speed_x']
            
            # Reiniciar partículas que salieron de pantalla
            if particle['y'] > c.ALTO:
                particle['y'] = -10
                particle['x'] = pygame.math.Vector2(particle['x'], 0).x
    
    def draw(self, screen):
        """Dibuja la pantalla de victoria."""
        # Fondo degradado oscuro
        for y in range(c.ALTO):
            progress = y / c.ALTO
            color_val = int(10 + progress * 30)
            pygame.draw.line(screen, (color_val, color_val - 5, color_val + 10), (0, y), (c.ANCHO, y))
        
        # Dibujar partículas
        for particle in self.particles:
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             particle['size'])
        
        # Aplicar fade in
        if self.phase == "fade_in":
            overlay = pygame.Surface((c.ANCHO, c.ALTO))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(255 - int(self.fade_alpha))
            screen.blit(overlay, (0, 0))
            return
        
        # Título principal
        title_text = "¡VICTORIA!"
        title_color = (255, 215, 0)  # Dorado
        
        # Efecto de brillo en el título
        glow_offset = int(5 * abs(pygame.math.Vector2(1, 0).rotate(self.timer * 2).x))
        
        # Sombra del título
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(c.ANCHO // 2 + 3, 100 + 3))
        screen.blit(title_shadow, shadow_rect)
        
        # Título principal
        title = self.title_font.render(title_text, True, title_color)
        title_rect = title.get_rect(center=(c.ANCHO // 2, 100))
        screen.blit(title, title_rect)
        
        # Revelación progresiva de información
        if self.text_reveal_progress > 0:
            y_offset = 200
            
            # Dificultad
            if self.text_reveal_progress > 0.2:
                diff_text = f"Dificultad: {self.difficulty_label}"
                diff_surf = self.subtitle_font.render(diff_text, True, (200, 255, 200))
                screen.blit(diff_surf, diff_surf.get_rect(center=(c.ANCHO // 2, y_offset)))
            
            # Intentos
            if self.text_reveal_progress > 0.4:
                intentos_text = f"Intentos: {self.intentos}"
                intentos_surf = self.text_font.render(intentos_text, True, (255, 255, 255))
                screen.blit(intentos_surf, intentos_surf.get_rect(center=(c.ANCHO // 2, y_offset + 60)))
            
            # Mensaje de estrella (si aplica)
            if self.text_reveal_progress > 0.6 and not self.is_practice:
                star_text = f"[STAR] ¡Estrella {self.difficulty_label} obtenida!"
                star_surf = self.text_font.render(star_text, True, (255, 215, 0))
                screen.blit(star_surf, star_surf.get_rect(center=(c.ANCHO // 2, y_offset + 120)))
            
            # Mensaje de práctica
            if self.text_reveal_progress > 0.6 and self.is_practice:
                practice_text = "Modo Práctica - Sin recompensas"
                practice_surf = self.small_font.render(practice_text, True, (180, 180, 180))
                screen.blit(practice_surf, practice_surf.get_rect(center=(c.ANCHO // 2, y_offset + 120)))
        
        # Opciones (solo cuando la animación termina)
        if self.can_select:
            options_y = 420
            for i, option in enumerate(self.options):
                selected = (i == self.selected_option)
                color = (255, 255, 255) if selected else (150, 150, 150)
                
                option_surf = self.text_font.render(option, True, color)
                option_rect = option_surf.get_rect(center=(c.ANCHO // 2, options_y + i * 50))
                
                if selected:
                    # Flecha indicadora
                    arrow = self.text_font.render(">", True, (85, 171, 77))
                    screen.blit(arrow, (option_rect.left - 40, option_rect.top))
                
                screen.blit(option_surf, option_rect)
            
            # Hint de controles
            hint = self.small_font.render("Usa ↑↓ para moverte, X/Enter para seleccionar", True, (120, 120, 120))
            screen.blit(hint, hint.get_rect(center=(c.ANCHO // 2, c.ALTO - 40)))
