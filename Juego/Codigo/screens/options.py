import os
import pygame
import Const as c


class OptionsMenu:
    def __init__(self, fullscreen=False, volume=0.5):
        self.fullscreen = fullscreen
        self.volume = float(max(0.0, min(1.0, volume)))
        self.options = ["Modo de pantalla", "Volumen música", "Volver"]
        self.index = 0
        self.title_font = pygame.font.Font(None, 60)
        self.opt_font = pygame.font.Font(None, 40)
        self.small = pygame.font.Font(None, 28)
        # Callbacks to apply settings (set by main)
        self.apply_fullscreen_cb = None
        self.apply_volume_cb = None
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
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if self.index == 1:  # volumen
                    self.volume = max(0.0, round(self.volume - 0.05, 2))
                    if self.apply_volume_cb:
                        self.apply_volume_cb(self.volume)
                    if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.index == 1:  # volumen
                    self.volume = min(1.0, round(self.volume + 0.05, 2))
                    if self.apply_volume_cb:
                        self.apply_volume_cb(self.volume)
                    if self.sfx_move: self.sfx_move.play()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_x):
                if self.index == 0:  # toggle fullscreen
                    self.fullscreen = not self.fullscreen
                    if self.apply_fullscreen_cb:
                        self.apply_fullscreen_cb(self.fullscreen)
                    if self.sfx_select: self.sfx_select.play()
                elif self.index == 2:  # Volver
                    if self.sfx_select: self.sfx_select.play()
                    return "back"

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((15, 18, 20))
        title = self.title_font.render("Opciones", True, (255, 230, 120))
        screen.blit(title, title.get_rect(center=(c.ANCHO // 2, 90)))

        # Modo de pantalla
        mode_text = "Pantalla completa" if self.fullscreen else "Modo ventana"
        txt0 = self.opt_font.render(f"Modo de pantalla: {mode_text}", True, (230, 230, 230))
        r0 = txt0.get_rect(center=(c.ANCHO // 2, 220))
        if self.index == 0:
            screen.blit(self.small.render("[Enter] para alternar", True, (255, 230, 120)), (r0.left, r0.bottom + 6))
        screen.blit(txt0, r0)

        # Volumen música
        txt1 = self.opt_font.render(f"Volumen música: {int(self.volume*100)}%", True, (230, 230, 230))
        r1 = txt1.get_rect(center=(c.ANCHO // 2, 300))
        if self.index == 1:
            hint = self.small.render("[←/→] ajusta el volumen", True, (255, 230, 120))
            screen.blit(hint, (r1.left, r1.bottom + 6))
        screen.blit(txt1, r1)

        # Volver
        txt2 = self.opt_font.render("Volver", True, (230 if self.index != 2 else 255, 230 if self.index != 2 else 255, 230))
        r2 = txt2.get_rect(center=(c.ANCHO // 2, 380))
        if self.index == 2:
            screen.blit(self.small.render("[Enter] para volver", True, (255, 230, 120)), (r2.left, r2.bottom + 6))
        screen.blit(txt2, r2)
