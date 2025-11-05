import os
import pygame
import Const as c


class PracticeMenu:
    def __init__(self):
        self.options = ["Fase 1", "Fase 2", "¿?", "Volver"]
        self.index = 0
        self.selected_phase = None  # 1 | 2 | 3 | 'back'
        self.title_font = pygame.font.Font(None, 60)
        self.opt_font = pygame.font.Font(None, 44)
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
                if choice.startswith("Fase 1"):
                    self.selected_phase = 1
                elif choice.startswith("Fase 2"):
                    self.selected_phase = 2
                elif choice.startswith("¿?"):
                    self.selected_phase = 3
                else:
                    self.selected_phase = "back"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((24, 24, 24))
        title = self.title_font.render("Practicar fases", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 120)))

        base_y = 240
        gap = 56
        for i, txt in enumerate(self.options):
            selected = (i == self.index)
            color = (255, 255, 255) if selected else (200, 200, 200)
            surf = self.opt_font.render(txt, True, color)
            rect = surf.get_rect(center=(c.ANCHO // 2, base_y + i * gap))
            if selected:
                arrow = self.opt_font.render(">", True, (85, 171, 77))
                screen.blit(arrow, (rect.left - 40, rect.top))
            screen.blit(surf, rect)
