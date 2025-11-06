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
        self.desc_font = pygame.font.Font(None, 28)
        # Cooldown para evitar auto-selección al entrar
        self.entry_cooldown = 10
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

        # Iconos mini para cada dificultad
        self.icon_junior = None
        self.icon_senior = None
        try:
            pth = os.path.join("Juego", "assets", "Sprites", "mini_junior.png")
            img = pygame.image.load(pth).convert_alpha()
            self.icon_junior = pygame.transform.smoothscale(img, (36, 36))
        except Exception:
            surf = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(surf, (80, 200, 80), (12, 12), 10)
            self.icon_junior = surf
        try:
            pth = os.path.join("Juego", "assets", "Sprites", "mini_senior.png")
            img = pygame.image.load(pth).convert_alpha()
            self.icon_senior = pygame.transform.smoothscale(img, (36, 36))
        except Exception:
            surf = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(surf, (200, 80, 80), (12, 12), 10)
            self.icon_senior = surf

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.index = (self.index - 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.index = (self.index + 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.index = (self.index - 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.index = (self.index + 1) % len(self.options)
                if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_x):
                if self.entry_cooldown > 0:
                    return
                choice = self.options[self.index]
                if self.sfx_select: self.sfx_select.play()
                if choice.startswith("Junior"):
                    self.selected_difficulty = "junior"
                elif choice.startswith("Senior"):
                    self.selected_difficulty = "senior"
                else:
                    self.selected_difficulty = "back"

    def update(self):
        if self.entry_cooldown > 0:
            self.entry_cooldown -= 1

    def draw(self, screen):
        screen.fill((18, 22, 30))
        title = self.title_font.render("Seleccionar dificultad", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 90)))

        # Descripción según opción seleccionada
        desc_text = ""
        if self.options[self.index].startswith("Junior"):
            desc_text = "Ideal para iniciantes"
        elif self.options[self.index].startswith("Senior"):
            desc_text = "Experiencia original, sin ventajas."

        if desc_text:
            desc = self.desc_font.render(desc_text, True, (220, 220, 220))
            screen.blit(desc, desc.get_rect(center=(c.ANCHO // 2, 150)))

        # Opciones en horizontal
        base_y = 380
        xs = [c.ANCHO // 2 - 220, c.ANCHO // 2, c.ANCHO // 2 + 220]
        for i, (txt, x) in enumerate(zip(self.options, xs)):
            selected = (i == self.index)
            color = (255, 255, 255) if selected else (200, 200, 200)
            surf = self.opt_font.render(txt, True, color)
            r = surf.get_rect(center=(x, base_y))
            screen.blit(surf, r)

            # Iconos al lado de Junior/Senior
            if selected:
                if txt.startswith("Junior") and self.icon_junior:
                    icon_rect = self.icon_junior.get_rect(midleft=(r.right + 10, r.centery))
                    screen.blit(self.icon_junior, icon_rect)
                elif txt.startswith("Senior") and self.icon_senior:
                    icon_rect = self.icon_senior.get_rect(midleft=(r.right + 10, r.centery))
                    screen.blit(self.icon_senior, icon_rect)

            # Selector visual (flecha) debajo
            if selected:
                arrow = self.opt_font.render("^", True, (85, 171, 77))
                a_rect = arrow.get_rect(center=(x, base_y + 30))
                screen.blit(arrow, a_rect)
