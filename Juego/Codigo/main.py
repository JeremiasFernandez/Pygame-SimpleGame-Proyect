import pygame, random, sys, os
import Const as c
import characters.player as p
import characters.bullet as bullet
import characters.boss as boss
import screens.gameover as gameover
from characters.border import Border
import screens.combat as combat

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

pygame.init()
pygame.mixer.init()

# --- Ventana ---
screen = pygame.display.set_mode((c.ANCHO, c.ALTO))
pygame.display.set_caption("Bossfight: The Trojan Virus")
clock = pygame.time.Clock()

# --- Grupos ---
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# --- Jugador ---
player = p.Player()
all_sprites.add(player)

# --- Variables globales ---
enemy = None
modo_juego = "intro"
font = pygame.font.Font(None, 36)
border = Border()
combate = None
intentos = 0

# --- Tutorial Hint (sprite arriba a la derecha con fadeout) ---
tutorial_hint_img = None
tutorial_hint_total = 10 * c.FPS  # ~10 segundos
tutorial_hint_ticks = 0

def _init_tutorial_hint():
    global tutorial_hint_img, tutorial_hint_ticks
    tutorial_hint_ticks = tutorial_hint_total
    if tutorial_hint_img is None:
        try:
            path = os.path.join("Juego", "assets", "Sprites", "tutorial_hint.png")
            img = pygame.image.load(path).convert_alpha()
            # Triplicar su tamaño explícitamente
            new_w = int(img.get_width() * 3)
            new_h = int(img.get_height() * 3)
            if new_w > 0 and new_h > 0:
                img = pygame.transform.smoothscale(img, (new_w, new_h))
            tutorial_hint_img = img
            print(f"ℹ️ Tutorial hint cargado: {path}")
        except Exception as e:
            tutorial_hint_img = None
            print(f"⚠️ No se pudo cargar tutorial_hint.png: {e}")

def _draw_tutorial_hint(screen, enemy):
    global tutorial_hint_ticks
    if tutorial_hint_ticks <= 0:
        return
    if tutorial_hint_img is None:
        # Fallback: cajita con texto
        alpha = int(200 * (tutorial_hint_ticks / tutorial_hint_total))
        box = pygame.Surface((220, 50), pygame.SRCALPHA)
        box.fill((20, 20, 40, alpha))
        txt = pygame.font.Font(None, 24).render("Usa X y esquiva!", True, (255, 255, 200))
        box.blit(txt, (10, 15))
        x = c.ANCHO - box.get_width() - 12
        y = 12
        # Si hay jefe, intentar ubicarla junto a su lado derecho
        if enemy:
            ex, ey, ew, eh = enemy.rect
            x = min(c.ANCHO - box.get_width() - 12, ex + ew + 40)
            y = max(12, ey + 60)
        screen.blit(box, (x, y))
    else:
        # Calcular alpha por fadeout lineal
        alpha = max(0, min(255, int(255 * (tutorial_hint_ticks / tutorial_hint_total))))
        img = tutorial_hint_img.copy()
        img.set_alpha(alpha)
        # Posicionar al lado del jefe (preferido) o en esquina sup. derecha
        x = c.ANCHO - img.get_width() - 12
        y = 12
        if enemy:
            ex, ey, ew, eh = enemy.rect
            # Más a la derecha y más abajo respecto del jefe
            x = min(c.ANCHO - img.get_width() - 12, ex + ew + 40)
            y = max(12, ey + 60)
        screen.blit(img, (x, y))
    # Decrementar contador por frame
    tutorial_hint_ticks -= 1

# ---------------------------------------------------------
def mostrar_texto(texto, color, y):
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(c.ANCHO // 2, y))
    screen.blit(render, rect)

# ---------------------------------------------------------
def reproducir_musica_aleatoria():
    """Selecciona y reproduce una canción de fase 1 al azar."""
    pygame.mixer.music.stop()
    versiones = ["phase1", "phase1B", "phase1C", "phase1D", "phase1E", "phase1F", "phase1G"]
    eleccion = random.choice(versiones)
    ruta = f"Juego/assets/Soundtrack/{eleccion}.mp3"
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        print(f"🎵 Música seleccionada: {eleccion}")
    except Exception as e:
        print(f"⚠️ No se pudo cargar la música {eleccion}: {e}")

# ---------------------------------------------------------
def reset_game():
    """Reinicia todo el combate."""
    global bullets, all_sprites, player, enemy, modo_juego, combate, intentos
    bullets.empty()
    all_sprites.empty()

    player = p.Player()
    all_sprites.add(player)

    enemy = boss.Boss(bullets, all_sprites)
    all_sprites.add(enemy)

    combate = combat.CombatSystem()
    modo_juego = "batalla"
    intentos += 1
    reproducir_musica_aleatoria()
    _init_tutorial_hint()

# ---------------------------------------------------------
running = True
titulo_troyano_timer = 0
titulo_font = pygame.font.Font(None, 80)

while running:
    clock.tick(c.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Botón de debug
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            if enemy:
                # Apply large debug damage via enemy.hit so transitions run
                try:
                    enemy.hit(100)
                except Exception:
                    enemy.hp -= 100
                print(f"💥 Boss HP reducido a {getattr(enemy,'hp',None)}")

        # Forzar ataque de lluvia para pruebas rápidas
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if enemy:
                enemy.current_attack = "attack_rain"
                enemy.attack_timer = 120
                print("⚡ Forzando ataque: attack_rain")

        # Iniciar batalla
        if event.type == pygame.KEYDOWN and modo_juego == "intro" and event.key == pygame.K_x:
            modo_juego = "batalla"
            enemy = boss.Boss(bullets, all_sprites)
            all_sprites.add(enemy)
            combate = combat.CombatSystem()
            intentos += 1
            reproducir_musica_aleatoria()
            _init_tutorial_hint()


    # -----------------------------------------------------
    # --- DIBUJO Y LÓGICA ---
    # -----------------------------------------------------

    if modo_juego == "batalla":
        if enemy and hasattr(enemy, "fondo_color"):
            screen.fill(((0, 0, 0)))
        else:
            screen.fill(c.NEGRO)

        # Fondo especial Fase 2
        if enemy and hasattr(enemy, "draw_phase2_background"):
            enemy.draw_phase2_background(screen)
        
        # Fondo especial Fase 3 (con muchas más partículas)
        if enemy and hasattr(enemy, "draw_phase3_background"):
            enemy.draw_phase3_background(screen)
    else:
        screen.fill((54, 0, 0))

    # --- Intro ---
    if modo_juego == "intro":
        mostrar_texto("Tu computadora tiene un VIRUS...", c.ROJO, c.ALTO // 2 - 50)
        mostrar_texto("Presiona [X] para enfrentarlo", c.BLANCO, c.ALTO // 2 + 20)

    # --- Batalla ---
    elif modo_juego == "batalla":
        keys = pygame.key.get_pressed()
        player.update(keys)
        combate.update(player, enemy)

        # Si el jefe marcó victoria lista, pasar a pantalla de victoria
        if enemy and getattr(enemy, 'victory_ready', False):
            pygame.mixer.music.stop()
            modo_juego = "victoria"
            bullets.empty()

        # Efecto de texto “TROYANO LEGENDARIO”
        if enemy and enemy.phase == 2:
            if titulo_troyano_timer == 0:
                titulo_troyano_timer = 150
            if titulo_troyano_timer > 0:
                titulo_troyano_timer -= 1
                texto = titulo_font.render("TROYANO LEGENDARIO", True, (255, 60, 60))
                escala = 1.0 + 0.02 * random.uniform(-1, 1)
                texto = pygame.transform.rotozoom(texto, random.uniform(-1, 1), escala)
                rect = texto.get_rect(center=(c.ANCHO // 2, 100))
                screen.blit(texto, rect)

        if combate.state == "menu":
            border.draw(screen)
            if enemy:
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)
                enemy.draw_flash_effect(screen)  # Flash blanco para fase 3
                # Asegurar que transiciones críticas (como fase 3) no se pierdan en 'menu'
                try:
                    enemy.check_phase3_transition()
                except Exception:
                    pass
                _draw_tutorial_hint(screen, enemy)
            combate.draw(screen, enemy)

        elif combate.state == "ataque":
            border.draw(screen)
            if enemy:
                screen.blit(enemy.image, enemy.rect)
                enemy.draw_health_bar(screen)
                enemy.draw_flash_effect(screen)  # Flash blanco para fase 3
                # También verificar transiciones durante 'ataque'
                try:
                    enemy.check_phase3_transition()
                except Exception:
                    pass
                _draw_tutorial_hint(screen, enemy)
            combate.draw(screen, enemy)

        elif combate.state == "defensa":
            # Primero actualizamos todo
            if enemy:
                # Guardar fase anterior para detectar cambio a fase 3
                prev_phase = enemy.phase
                enemy.update()
                enemy.check_phase3_transition()
                # Si acabamos de entrar a fase 3, curar al jugador completamente
                if prev_phase != 3 and enemy.phase == 3 and hasattr(enemy, '_fase3_activada'):
                    player.hp = 20  # Vida completa
                    print("💚 Jugador curado completamente al activarse fase 3")
            bullets.update()
            border.update(player)

            # Colisiones
            hits = pygame.sprite.spritecollide(player, bullets, True)
            for hit in hits:
                damage = getattr(hit, "damage", 5)
                player.take_damage(damage)

            # Dibujado en orden correcto
            border.draw(screen)
            # Barra delgada de tiempo de defensa (encima del border)
            if hasattr(combate, 'draw_defense_timer_bar'):
                combate.draw_defense_timer_bar(screen)
            
            # Dibujar indicador de spearcross (antes del jefe para que quede detrás)
            if enemy and hasattr(enemy, 'draw_cross_indicator'):
                enemy.draw_cross_indicator(screen)
            
            screen.blit(enemy.image, enemy.rect)  # Primero el jefe
            bullets.draw(screen)  # Luego las balas
            screen.blit(player.image, player.rect)  # Luego el jugador
            
            # Por último las UI
            player.draw_health_bar(screen)
            if enemy:
                enemy.draw_health_bar(screen)
                enemy.draw_flash_effect(screen)  # Flash blanco para fase 3
                _draw_tutorial_hint(screen, enemy)

            if player.hp <= 0:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load("Juego/assets/Soundtrack/GameOver.mp3")
                    pygame.mixer.music.set_volume(0.4)
                    pygame.mixer.music.play(0)
                except Exception as e:
                    print("Error al reproducir GameOver:", e)
                gameover.game_over_screen(screen, clock)
                reset_game()

    elif modo_juego == "victoria":
        screen.fill((10, 10, 20))
        titulo = pygame.font.Font(None, 80).render("¡VICTORIA!", True, (255, 230, 120))
        subt  = pygame.font.Font(None, 36).render("(Pantalla final en construcción)", True, (220, 220, 220))
        screen.blit(titulo, titulo.get_rect(center=(c.ANCHO//2, c.ALTO//2 - 20)))
        screen.blit(subt,   subt.get_rect(center=(c.ANCHO//2, c.ALTO//2 + 30)))

    # --- Contador de intentos ---
    if intentos > 0:
        font_small = pygame.font.Font(None, 22)
        text = f"Intentos: {intentos}"
        txt_surface = font_small.render(text, True, (220, 220, 220))
        alpha_surf = pygame.Surface(txt_surface.get_size(), pygame.SRCALPHA)
        alpha_surf.fill((0, 0, 0, 60))
        alpha_surf.blit(txt_surface, (0, 0))
        x = c.ANCHO - txt_surface.get_width() - 15
        y = c.ALTO - 25
        screen.blit(alpha_surf, (x, y))

    pygame.display.flip()

pygame.quit()
sys.exit()
