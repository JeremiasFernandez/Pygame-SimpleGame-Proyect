import os
import pygame
import Const as c


class PracticeMenu:
    def __init__(self, has_two_stars: bool = False, secret_unlocked: bool = False):
        self.has_two_stars = bool(has_two_stars)
        # secret_unlocked derivado de estrellas (true si ambas)
        self.secret_unlocked = bool(secret_unlocked or has_two_stars)
        # Añadir jefe secreto (bloqueado si no hay 2 estrellas)
        if self.secret_unlocked:
            self.options = ["Fase 1", "Fase 2", "Fase 3 (End)", "Jefe Secreto", "Volver"]
        else:
            self.options = ["Fase 1", "Fase 2", "Fase 3 (End)", "Jefe Secreto (Bloqueado)", "Volver"]
        
        self.index = 0
        self.selected_phase = None  # 1 | 2 | 3 | 'back'
        self.title_font = pygame.font.Font(None, 60)
        self.opt_font = pygame.font.Font(None, 44)
        
        # Mensajes temporales
        self.message_text = ""
        self.message_color = (255, 255, 255)
        self.message_timer = 0  # frames
        
        # Evita que la pulsación de X/Enter que te trajo aquí dispare selección inmediata
        self.entry_cooldown = 10  # ~10 frames (~0.16s a 60 FPS)
        
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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.index = (self.index - 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.index = (self.index + 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_x):
                # Bloqueo inicial: ignorar selección durante los primeros frames tras entrar
                if self.entry_cooldown > 0:
                    return
                
                choice = self.options[self.index]
                print(f"[DEBUG PRACTICE] Opción seleccionada: '{choice}' (index={self.index})")
                if self.sfx_select: self.sfx_select.play()
                
                # Fase 1
                if choice.startswith("Fase 1"):
                    self.selected_phase = 1
                    print("[DEBUG PRACTICE] -> selected_phase = 1")
                
                # Fase 2
                elif choice.startswith("Fase 2"):
                    self.selected_phase = 2
                    print("[DEBUG PRACTICE] -> selected_phase = 2")
                
                # Fase 3 (siempre disponible)
                elif choice.startswith("Fase 3"):
                    self.selected_phase = 3
                    print("[DEBUG PRACTICE] -> selected_phase = 3")

                # Jefe Secreto (requiere dos estrellas)
                elif choice.startswith("Jefe Secreto"):
                    print(f"[DEBUG PRACTICE] choice='{choice}', secret_unlocked={self.secret_unlocked}, has_two_stars={self.has_two_stars}")
                    if self.secret_unlocked and not "Bloqueado" in choice:
                        self.selected_phase = "secret_boss"
                        print("[DEBUG PRACTICE] Estableciendo selected_phase='secret_boss'")
                    else:
                        self._show_message("Se requieren 2 estrellas", (255,60,60))
                        print("[DEBUG PRACTICE] Mostrando mensaje de bloqueo")
                
                # Volver
                elif choice == "Volver":
                    self.selected_phase = "back"

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        if self.entry_cooldown > 0:
            self.entry_cooldown -= 1
        # Actualizar opciones si se desbloqueó mientras está abierto
        if self.secret_unlocked and any("Bloqueado" in o for o in self.options):
            self.options = ["Fase 1", "Fase 2", "Fase 3 (End)", "Jefe Secreto", "Volver"]

    def _show_message(self, text, color):
        self.message_text = text
        self.message_color = color
        self.message_timer = 120  # ~2s

    def draw(self, screen):
        screen.fill((24, 24, 24))
        title = self.title_font.render("Practicar fases", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 120)))

        base_y = 240
        gap = 56
        for i, txt in enumerate(self.options):
            selected = (i == self.index)
            color = (255, 255, 255) if selected else (200, 200, 200)
            if "Bloqueado" in txt:
                color = (150, 70, 70) if selected else (120, 50, 50)
            
            surf = self.opt_font.render(txt, True, color)
            rect = surf.get_rect(center=(c.ANCHO // 2, base_y + i * gap))
            
            if selected:
                arrow = self.opt_font.render(">", True, (85, 171, 77))
                screen.blit(arrow, (rect.left - 40, rect.top))
            
            screen.blit(surf, rect)

        # Mensaje temporal (errores / bloqueos)
        if self.message_timer > 0 and self.message_text:
            msg_font = pygame.font.Font(None, 36)
            m_surf = msg_font.render(self.message_text, True, self.message_color)
            m_rect = m_surf.get_rect(center=(c.ANCHO // 2, c.ALTO - 80))
            # Fondo rojo translúcido si es error
            if self.message_color[0] > 200 and self.message_color[1] < 100:
                bg = pygame.Surface((m_rect.width + 40, m_rect.height + 20), pygame.SRCALPHA)
                bg.fill((self.message_color[0], self.message_color[1], self.message_color[2], 90))
                bg_rect = bg.get_rect(center=m_rect.center)
                screen.blit(bg, bg_rect)
            screen.blit(m_surf, m_rect)
