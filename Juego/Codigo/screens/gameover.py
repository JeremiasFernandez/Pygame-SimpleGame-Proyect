import pygame, sys, math, random
import Const as c

def game_over_screen(screen, clock):
    # --- detener música previa y reproducir la triste ---
    try:
        pygame.mixer.music.stop()
        sad = pygame.mixer.Sound("Juego/assets/Soundtrack/GameOver.mp3")
        sad.set_volume(0.6)
        sad.play(-1)
    except Exception:
        pass

    font_big = pygame.font.Font(None, 70)
    font_small = pygame.font.Font(None, 38)

    t0 = pygame.time.get_ticks()
    esperando = True
    alpha_fondo = 0
    y_text = c.ALTO // 2 - 200  # empieza arriba
    y_final = c.ALTO // 2 - 40

    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        # --- fondo oscuro progresivo ---
        screen.fill((0, 0, 20))
        alpha_fondo = min(200, alpha_fondo + 2)
        overlay = pygame.Surface((c.ANCHO, c.ALTO))
        overlay.fill((10, 0, 30))
        overlay.set_alpha(alpha_fondo)
        screen.blit(overlay, (0, 0))

        # tiempo relativo
        t = (pygame.time.get_ticks() - t0) / 1000.0

        # --- animación del texto ---
        # caída suave
        y_text = y_final - 60 * math.exp(-t * 1.5)
        # leve “respiración” (zoom sutil)
        scale = 1.0 + 0.02 * math.sin(t * 1.2)
        shake_x = int(2 * math.sin(t * 0.8))
        shake_y = int(1 * math.cos(t * 1.5))

        # render principal
        text_surface = font_big.render("DERROTA HUMILLANTE", True, (200, 80, 80))
        w, h = text_surface.get_size()
        text_surface = pygame.transform.smoothscale(text_surface, (int(w * scale), int(h * scale)))
        rect = text_surface.get_rect(center=(c.ANCHO // 2 + shake_x, int(y_text) + shake_y))
        screen.blit(text_surface, rect)

        # subtítulo parpadeante suave
        blink = (math.sin(t * 2.5) + 1) / 2
        msg = "Presiona [ESPACIO] para reiniciar o [ESC] para salir"
        sub = font_small.render(msg, True, (180, 180, 200))
        sub.set_alpha(int(90 + 165 * blink))
        sub_rect = sub.get_rect(center=(c.ANCHO // 2, c.ALTO // 2 + 40))
        screen.blit(sub, sub_rect)

        # --- pequeñas partículas flotando ---
        for _ in range(2):
            x = random.randint(0, c.ANCHO)
            y = random.randint(0, c.ALTO)
            color = (80, 50, 90)
            pygame.draw.circle(screen, color, (x, y), 1)

        pygame.display.flip()
        clock.tick(c.FPS)

    try:
        sad.stop()
    except Exception:
        pass
