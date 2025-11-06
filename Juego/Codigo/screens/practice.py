import os
import pygame
import Const as c


class PracticeMenu:
    def __init__(self, has_two_stars: bool = False):
        # Agregamos cuarta opción "Locked" y movemos "Volver" al final
        self.options = ["Fase 1", "Fase 2", "End", "Bloqueado", "Volver"]
        self.index = 0
        self.selected_phase = None  # 1 | 2 | 3 | 'back'
        self.title_font = pygame.font.Font(None, 60)
        self.opt_font = pygame.font.Font(None, 44)
        self.has_two_stars = bool(has_two_stars)
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
                if self.sfx_select: self.sfx_select.play()
                if choice.startswith("Fase 1"):
                    self.selected_phase = 1
                elif choice.startswith("Fase 2"):
                    self.selected_phase = 2
                elif choice.startswith("¿?"):
                    self.selected_phase = 3
                elif choice == "Unlocked":
                    # Comprobar estrellas
                    if not self.has_two_stars:
                        self.message_text = "Necesitas 2 estrellas para entrar aqui"
                        self.message_color = c.ROJO
                        self.message_timer = 180
                    else:
                        self.message_text = "Secret boss"
                        self.message_color = (200, 255, 200)
                        self.message_timer = 180
                else:
                    self.selected_phase = "back"

    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        if self.entry_cooldown > 0:
            self.entry_cooldown -= 1

    def draw(self, screen):
        screen.fill((24, 24, 24))
        title = self.title_font.render("Practicar fases", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 120)))

        base_y = 240
        gap = 56
        for i, txt in enumerate(self.options):
            selected = (i == self.index)
            # Forzar gris para la opción "Unlocked"
            if txt == "Unlocked":
                color = (150, 150, 150)
            else:
                color = (255, 255, 255) if selected else (200, 200, 200)
            surf = self.opt_font.render(txt, True, color)
            rect = surf.get_rect(center=(c.ANCHO // 2, base_y + i * gap))
            if selected:
                arrow = self.opt_font.render(">", True, (85, 171, 77))
                screen.blit(arrow, (rect.left - 40, rect.top))
            screen.blit(surf, rect)

        # Mostrar mensaje temporal si existe
        if self.message_timer > 0 and self.message_text:
            msg_font = pygame.font.Font(None, 36)
            msg_surf = msg_font.render(self.message_text, True, self.message_color)
            msg_rect = msg_surf.get_rect(center=(c.ANCHO // 2, base_y + len(self.options) * gap - 10))
            screen.blit(msg_surf, msg_rect)
