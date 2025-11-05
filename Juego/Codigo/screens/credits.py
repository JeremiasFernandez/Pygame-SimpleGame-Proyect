import os
import pygame
import Const as c


class CreditsScreen:
    def __init__(self, text=None):
        self.text = text or "Creado por: Jeremias Fernandez, 2025.\n\nAgradecimientos especiales a:\n- La UTN.\n- Mi primo bauti.\n\n¡Gracias por jugar!"
        self.title_font = pygame.font.Font(None, 60)
        self.text_font = pygame.font.Font(None, 28)
        # Sonidos
        self.sfx_select = None
        try:
            sel_path = os.path.join("Juego", "assets", "Sounds", "menu_select.wav")
            self.sfx_select = pygame.mixer.Sound(sel_path)
            self.sfx_select.set_volume(0.6)
        except Exception:
            self.sfx_select = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_x):
            if self.sfx_select: self.sfx_select.play()
            return "back"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((12, 12, 14))
        title = self.title_font.render("Créditos", True, (85, 171, 77))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 80)))

        # Caja
        box_w, box_h = int(c.ANCHO * 0.7), int(c.ALTO * 0.5)
        box = pygame.Rect(0, 0, box_w, box_h)
        box.center = (c.ANCHO // 2, c.ALTO // 2 + 20)
        pygame.draw.rect(screen, (30, 30, 40), box)
        pygame.draw.rect(screen, (120, 120, 160), box, 3)

        # Renderizar texto con saltos de línea
        y = box.top + 18
        for line in self.text.splitlines():
            surf = self.text_font.render(line, True, (217, 255, 214))
            screen.blit(surf, (box.left + 18, y))
            y += 28

        hint = self.text_font.render("[Enter] Volver", True, (255, 230, 120))
        screen.blit(hint, (box.left + 18, box.bottom - 30))
