import os
import pygame
import Const as c


class MainMenu:
    def __init__(self):
        self.options = ["Jugar", "Practicar", "Opciones", "Créditos"]
        self.index = 0
        self.next_state = None  # 'play_select' | 'practice' | 'options' | 'credits'
        self.title_font = pygame.font.Font(None, 80)
        self.opt_font = pygame.font.Font(None, 44)
        self.version_font = pygame.font.Font(None, 24)
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
                choice = self.options[self.index]
                if self.sfx_select: self.sfx_select.play()
                if choice == "Jugar":
                    self.next_state = "play_select"
                elif choice == "Practicar":
                    self.next_state = "practice"
                elif choice == "Opciones":
                    self.next_state = "options"
                elif choice == "Créditos":
                    self.next_state = "credits"

    def update(self):
        pass

    def draw(self, screen):
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
        ver_text = "v0.6.2 (Pre-alpha)"
        ver_surf = self.version_font.render(ver_text, True, (220, 220, 230))
        ver_surf.set_alpha(140)
        vx = c.ANCHO - ver_surf.get_width() - 12
        vy = c.ALTO - ver_surf.get_height() - 10
        screen.blit(ver_surf, (vx, vy))
