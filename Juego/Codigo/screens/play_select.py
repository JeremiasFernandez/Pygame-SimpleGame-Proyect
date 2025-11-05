import os
import pygame
import Const as c


class PlaySelect:
    def __init__(self):
        self.options = ["Junior", "Senior", "Volver"]
        self.index = 0
        self.selected_difficulty = None  # 'junior' | 'senior'
        self.title_font = pygame.font.Font(None, 60)
        self.opt_font = pygame.font.Font(None, 44)
        # Cargar imagen del boss
        self.boss_img = None
        try:
            path = os.path.join("Juego", "assets", "Sprites", "Boss_Virus_1.png")
            img = pygame.image.load(path).convert_alpha()
            # Escalar a un tamaño amigable
            w = min(280, img.get_width())
            h = int(img.get_height() * (w / img.get_width()))
            self.boss_img = pygame.transform.smoothscale(img, (w, h))
        except Exception:
            self.boss_img = None
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
                if choice.startswith("Junior"):
                    self.selected_difficulty = "junior"
                elif choice.startswith("Senior"):
                    self.selected_difficulty = "senior"
                else:
                    self.selected_difficulty = "back"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((18, 22, 30))
        title = self.title_font.render("Selecciona dificultad", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 80)))

        # Imagen del boss al centro
        if self.boss_img:
            rect = self.boss_img.get_rect(center=(c.ANCHO // 2, 200))
            screen.blit(self.boss_img, rect)
        else:
            # Fallback: cuadro
            rect = pygame.Rect(0, 0, 260, 180)
            rect.center = (c.ANCHO // 2, 220)
            pygame.draw.rect(screen, (60, 60, 80), rect)
            pygame.draw.rect(screen, (120, 120, 160), rect, 3)

        base_y = 380
        gap = 54
        for i, txt in enumerate(self.options):
            selected = (i == self.index)
            color = (255, 255, 255) if selected else (200, 200, 200)
            surf = self.opt_font.render(txt, True, color)
            r = surf.get_rect(center=(c.ANCHO // 2, base_y + i * gap))
            if selected:
                arrow = self.opt_font.render(">", True, (85, 171, 77))
                screen.blit(arrow, (r.left - 40, r.top))
            screen.blit(surf, r)
