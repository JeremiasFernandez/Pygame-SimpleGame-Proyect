"""
main.py - Punto de Entrada del Juego
====================================
Bossfight: El Troyano
Juego de combate contra un virus informático con mecánicas de esquiva y ataques.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pygame
import random
import sys
import os

# ============================================================================
# FIX PARA PYINSTALLER - Ajustar rutas de assets
# ============================================================================
if getattr(sys, 'frozen', False):
    # Ejecutándose como .exe compilado
    # PyInstaller extrae archivos a sys._MEIPASS
    os.chdir(sys._MEIPASS)
else:
    # Ejecutándose como script Python - ir a la raíz del proyecto
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# Módulos del juego
import Const as c
import characters.player as p
import characters.bullet as bullet
import characters.boss as boss
from characters.border import Border

# Pantallas del juego
import screens.gameover as gameover
import screens.menu as menu_screen
import screens.play_select as play_select
import screens.practice as practice_screen
import screens.options as options_screen
import screens.credits as credits_screen
import screens.intro as intro_screen
import screens.victory as victory_screen
import screens.combat as combat


# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
# Inicializar Pygame
pygame.init()
pygame.mixer.init()


# ============================================================================
# VENTANA Y RELOJ
# ============================================================================
screen = pygame.display.set_mode((c.ANCHO, c.ALTO))
pygame.display.set_caption("Bossfight: El troyano")
clock = pygame.time.Clock()


# ============================================================================
# GRUPOS DE SPRITES
# ============================================================================
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()


# ============================================================================
# ENTIDADES PRINCIPALES
# ============================================================================
player = p.Player()
all_sprites.add(player)
enemy = None
border = Border()
combate = None


# ============================================================================
# VARIABLES GLOBALES DEL JUEGO
# ============================================================================
# Estado del juego
modo_juego = "menu"  # Estados: menu, intro, batalla, victoria, etc.
running = True
intentos = 0
is_practice_mode = False

# Configuración de audio
music_volume = 0.5
current_music_tag = None  # Tags: 'menu', 'menu_complete', 'battle'

# Configuración de pantalla
fullscreen = False

# Dificultad
difficulty_label = "Senior"
difficulty_factor = 1.0

# Estrellas de logros (persistentes entre partidas)
stars_junior = False
stars_senior = False

# UI y efectos
esc_cooldown = 0  # Prevenir doble-ESC accidental
titulo_troyano_timer = 0
font = pygame.font.Font(None, 36)
titulo_font = pygame.font.Font(None, 80)


# ============================================================================
# PANTALLAS INSTANCIADAS
# ============================================================================
main_menu = menu_screen.MainMenu()
playselect = None
practicemenu = None
optsmenu = None
creditss = None
introscreen = None
victoryscreen = None


# ============================================================================
# TUTORIAL HINT (Sprite temporal con fadeout)
# ============================================================================
tutorial_hint_img = None
tutorial_hint_total = 10 * c.FPS  # ~10 segundos
tutorial_hint_ticks = 0


# ============================================================================
# ANIMACIÓN DE ESTRELLAS (GIF)
# ============================================================================
star_frames = []
star_frame_index = 0
star_frame_timer = 0
star_frame_delay = 5  # Frames entre cada cambio de imagen


# ============================================================================
# FUNCIONES DE CARGA DE RECURSOS
# ============================================================================
def _load_star_gif():
    """
    Carga el GIF de la estrella y extrae todos sus frames para animación.
    Si falla, intenta cargar el PNG estático como fallback.
    """
    global star_frames
    if star_frames:
        return
    
    try:
        from PIL import Image
        gif_path = os.path.join("Juego", "assets", "Sprites", "star.gif")
        gif = Image.open(gif_path)
        frames = []
        
        try:
            while True:
                frame = gif.convert("RGBA")
                frame = frame.resize((60, 60), Image.Resampling.LANCZOS)
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                py_img = pygame.image.fromstring(data, size, mode)
                frames.append(py_img)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        
        star_frames = frames
        print(f"[STAR] Star GIF cargado: {len(frames)} frames")
    except ImportError:
        print("[WARNING] PIL/Pillow no disponible, usando PNG estatico")
        _load_star_png()
    except Exception as e:
        print(f"[WARNING] No se pudo cargar star.gif: {e}, usando PNG estatico")
        _load_star_png()


def _load_star_png():
    """Fallback: carga star.png como único frame estático."""
    global star_frames
    try:
        png_path = os.path.join("Juego", "assets", "Sprites", "star.png")
        img = pygame.image.load(png_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (40, 40))
        star_frames = [img]
        print("[STAR] Star PNG cargado como fallback")
    except Exception as e:
        print(f"[WARNING] No se pudo cargar star.png: {e}")
        star_frames = []


def _init_tutorial_hint():
    """Inicializa el hint/sprite del tutorial con fadeout temporal."""
    global tutorial_hint_img, tutorial_hint_ticks
    tutorial_hint_ticks = tutorial_hint_total
    
    if tutorial_hint_img is None:
        try:
            path = os.path.join("Juego", "assets", "Sprites", "tutorial_hint.png")
            img = pygame.image.load(path).convert_alpha()
            # Triplicar tamaño
            new_w = int(img.get_width() * 3)
            new_h = int(img.get_height() * 3)
            if new_w > 0 and new_h > 0:
                img = pygame.transform.smoothscale(img, (new_w, new_h))
            tutorial_hint_img = img
            print(f"[INFO] Tutorial hint cargado: {path}")
        except Exception as e:
            tutorial_hint_img = None
            print(f"[WARNING] No se pudo cargar tutorial_hint.png: {e}")


# ============================================================================
# FUNCIONES DE RENDERIZADO
# ============================================================================
def _draw_stars(screen):
    """Dibuja las estrellas animadas en el menú principal."""
    global star_frame_index, star_frame_timer
    
    if not (stars_junior or stars_senior):
        return
    
    if not star_frames:
        _load_star_gif()
    if not star_frames:
        return
    
    # Animar frame
    star_frame_timer += 1
    if star_frame_timer >= star_frame_delay:
        star_frame_timer = 0
        star_frame_index = (star_frame_index + 1) % len(star_frames)
    
    current_frame = star_frames[star_frame_index]
    base_x = c.ANCHO // 2 - 50
    base_y = 30  # Por encima del título del menú
    
    if stars_junior:
        screen.blit(current_frame, (base_x, base_y))
    if stars_senior:
        screen.blit(current_frame, (base_x + 60, base_y))


def _draw_tutorial_hint(screen, enemy):
    """Dibuja el hint del tutorial con fadeout progresivo."""
    global tutorial_hint_ticks
    
    if tutorial_hint_ticks <= 0:
        return
    
    if tutorial_hint_img is None:
        # Fallback: caja con texto
        alpha = int(200 * (tutorial_hint_ticks / tutorial_hint_total))
        box = pygame.Surface((220, 50), pygame.SRCALPHA)
        box.fill((20, 20, 40, alpha))
        txt = pygame.font.Font(None, 24).render("Usa X y esquiva!", True, (255, 255, 200))
        box.blit(txt, (10, 15))
        x = c.ANCHO - box.get_width() - 12
        y = 12
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
        x = c.ANCHO - img.get_width() - 12
        y = 12
        if enemy:
            ex, ey, ew, eh = enemy.rect
            x = min(c.ANCHO - img.get_width() - 12, ex + ew + 40)
            y = max(12, ey + 60)
        screen.blit(img, (x, y))
    
    # Decrementar contador
    tutorial_hint_ticks -= 1


def mostrar_texto(texto, color, y):
    """Renderiza y centra un texto en la pantalla."""
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(c.ANCHO // 2, y))
    screen.blit(render, rect)


# ============================================================================
# FUNCIONES DE AUDIO
# ============================================================================
def reproducir_musica_aleatoria():
    """Selecciona y reproduce una canción de fase 1 al azar."""
    global current_music_tag
    
    pygame.mixer.music.stop()
    versiones = ["phase1", "phase1B", "phase1C", "phase1D", "phase1E", "phase1F", "phase1G", "phase1H"]
    eleccion = random.choice(versiones)
    ruta = f"Juego/assets/Soundtrack/{eleccion}.mp3"
    
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        current_music_tag = "battle"
        print(f"[MUSIC] Musica seleccionada: {eleccion}")
    except Exception as e:
        print(f"[WARNING] No se pudo cargar la musica {eleccion}: {e}")


def play_menu_music_if_needed():
    """Reproduce la música del menú apropiada según los logros desbloqueados."""
    global current_music_tag
    
    # Determinar qué música debería estar sonando
    if stars_junior and stars_senior:
        target_tag = "menu_complete"
        ruta = "Juego/assets/Soundtrack/menu_theme_complete.mp3"
        msg = "[MUSIC] Musica de menu COMPLETA: menu_theme_complete.mp3"
    else:
        target_tag = "menu"
        ruta = "Juego/assets/Soundtrack/menu_theme.mp3"
        msg = "[MUSIC] Musica de menu reproduciendo: menu_theme.mp3"
    
    # Si ya está sonando la correcta, no hacer nada
    if current_music_tag == target_tag:
        return
    
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        current_music_tag = target_tag
        print(msg)
    except Exception as e:
        print(f"[WARNING] No se pudo reproducir musica de menu: {e}")


# ============================================================================
# FUNCIONES DE CONTROL DEL JUEGO
# ============================================================================
def reset_game():
    """Reinicia completamente el combate (para reintentar tras game over)."""
    global bullets, all_sprites, player, enemy, modo_juego, combate, intentos
    
    bullets.empty()
    all_sprites.empty()

    player = p.Player()
    all_sprites.add(player)

    enemy = boss.Boss(bullets, all_sprites, music_volume)
    all_sprites.add(enemy)
    
    try:
        enemy.difficulty = difficulty_factor
    except Exception:
        pass

    combate = combat.CombatSystem()
    modo_juego = "batalla"
    intentos += 1
    reproducir_musica_aleatoria()
    _init_tutorial_hint()


def apply_fullscreen(value: bool):
    """Aplica o desactiva el modo de pantalla completa."""
    global screen, fullscreen
    fullscreen = bool(value)
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((c.ANCHO, c.ALTO), flags)


def apply_music_volume(value: float):
    """Ajusta el volumen de la música."""
    global music_volume
    music_volume = max(0.0, min(1.0, float(value)))
    try:
        pygame.mixer.music.set_volume(music_volume)
    except Exception:
        pass


def start_battle(practice_phase: int | None = None):
    """
    Inicia una batalla desde el menú o el modo práctica.
    
    Args:
        practice_phase: Fase a practicar (1, 2, 3), o None para batalla normal.
    """
    global bullets, all_sprites, player, enemy, modo_juego, combate, intentos
    global is_practice_mode, current_music_tag
    
    # Limpiar y reiniciar entidades
    bullets.empty()
    all_sprites.empty()
    
    player = p.Player()
    all_sprites.add(player)
    
    enemy = boss.Boss(bullets, all_sprites, music_volume)
    all_sprites.add(enemy)
    
    try:
        enemy.difficulty = difficulty_factor
    except Exception:
        pass
    
    combate = combat.CombatSystem()
    modo_juego = "batalla"
    intentos += 1
    is_practice_mode = (practice_phase is not None)
    
    # Configurar música según fase
    try:
        if practice_phase == 2:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Juego/assets/Soundtrack/phase2.mp3")
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(-1)
            current_music_tag = "battle"
        elif practice_phase == 3:
            pass  # La fase 3 maneja su propia música
        else:
            reproducir_musica_aleatoria()
    except Exception as e:
        print(f"[WARNING] Error configurando musica inicial de practica: {e}")
    
    _init_tutorial_hint()
    
    # Ajustes de fase para modo práctica
    if practice_phase == 2:
        try:
            enemy._enter_phase2()
        except Exception:
            enemy.phase = 2
            enemy.hp = 120
    elif practice_phase == 3:
        try:
            enemy._activar_fase3()
        except Exception:
            enemy.phase = 3
            enemy.hp = 70
            enemy.difficulty = max(getattr(enemy, 'difficulty', 1.0), 1.6)


# ============================================================================
# INICIALIZACIÓN
# ============================================================================
# Iniciar música de menú al arrancar
play_menu_music_if_needed()


# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================
while running:
    clock.tick(c.FPS)
    # Reducir cooldown de ESC cada frame
    if esc_cooldown > 0:
        esc_cooldown -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Abrir chat en batalla al presionar C (manejo por evento para prioridad sobre ESC)
        if (modo_juego == "batalla" and combate and not getattr(combate, 'chat_active', False)
            and getattr(combate, 'state', None) == "menu"
            and event.type == pygame.KEYDOWN and event.key == pygame.K_c):
            try:
                combate.start_chat()
            except Exception as _e:
                pass
            # No procesar otros manejos para este evento
            continue
        
        # Si estamos en batalla y el chat está activo, manejar eventos del chat
        if modo_juego == "batalla" and combate and combate.chat_active:
            combate.handle_chat_event(event)
            continue  # No procesar otros eventos mientras el chat está activo
        
        # ESC: vuelve al menú desde cualquier pantalla EXCEPTO cuando ya estás en el menú (ahí sale del juego)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Anti-repeat: si aún está en cooldown, ignorar
            if esc_cooldown > 0:
                continue
            # Establecer cooldown ~0.3s
            try:
                esc_cooldown = max(8, c.FPS // 3)
            except Exception:
                esc_cooldown = 18
            if modo_juego == "menu":
                # Si estás en el menú, ESC cierra el juego
                running = False
            elif modo_juego == "batalla":
                # Desde batalla, limpiar y volver al menú
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                bullets.empty()
                all_sprites.empty()
                enemy = None
                combate = None
                modo_juego = "menu"
                try:
                    current_music_tag = None
                except Exception:
                    pass
                play_menu_music_if_needed()
            elif modo_juego == "victoria":
                # Desde victoria, volver al menú
                modo_juego = "menu"
                try:
                    current_music_tag = None
                except Exception:
                    pass
                play_menu_music_if_needed()
            elif modo_juego in ("intro", "play_select", "practice", "options", "credits"):
                # Desde cualquier otra pantalla, volver al menú
                modo_juego = "menu"
                playselect = None
                practicemenu = None
                optsmenu = None
                creditss = None
                play_menu_music_if_needed()

        # Botón de debug
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            if enemy:
                # Apply large debug damage via enemy.hit so transitions run
                try:
                    enemy.hit(100)
                except Exception:
                    enemy.hp -= 100
                print(f"💥 Boss HP reducido a {getattr(enemy,'hp',None)}")

        # CHEAT: Desbloquear todas las estrellas para testing (F2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            stars_junior = True
            stars_senior = True
            print("⭐⭐ CHEAT: Estrellas desbloqueadas!")
            play_menu_music_if_needed()

        # Forzar ataque de lluvia para pruebas rápidas
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if enemy:
                enemy.current_attack = "attack_rain"
                enemy.attack_timer = 120
                print("⚡ Forzando ataque: attack_rain")

        # Nuevo flujo de pantallas
        if modo_juego == "menu":
            main_menu.handle_event(event)
            if main_menu.next_state:
                if main_menu.next_state == "play_select":
                    playselect = play_select.PlaySelect()
                    modo_juego = "play_select"
                    play_menu_music_if_needed()
                elif main_menu.next_state == "practice":
                    practicemenu = practice_screen.PracticeMenu(has_two_stars=(stars_junior and stars_senior))
                    modo_juego = "practice"
                    play_menu_music_if_needed()
                elif main_menu.next_state == "options":
                    optsmenu = options_screen.OptionsMenu(fullscreen, music_volume)
                    optsmenu.apply_fullscreen_cb = apply_fullscreen
                    optsmenu.apply_volume_cb = apply_music_volume
                    modo_juego = "options"
                    play_menu_music_if_needed()
                elif main_menu.next_state == "credits":
                    creditss = credits_screen.CreditsScreen()
                    modo_juego = "credits"
                    play_menu_music_if_needed()
                main_menu.next_state = None

        # Cheat UTNFRA en menú (activar modo completo)
        if event.type == pygame.KEYDOWN and modo_juego == "menu":
            try:
                if p.process_menu_cheat_key(event.key):
                    # Activar estrellas y cambiar música del menú a 'complete'
                    stars_junior = True
                    stars_senior = True
                    pygame.mixer.music.stop()
                    current_music_tag = None
                    play_menu_music_if_needed()
                    print("[CHEAT] Modo completo activado por codigo UTNFRA")
            except Exception as e:
                print(f"[WARNING] Error procesando cheat: {e}")

        elif modo_juego == "play_select":
            playselect.handle_event(event)
            if playselect.selected_difficulty:
                if playselect.selected_difficulty == "junior":
                    difficulty_label = "Junior"; difficulty_factor = 0.55
                    modo_juego = "intro"
                    is_practice_mode = False  # No es práctica
                elif playselect.selected_difficulty == "senior":
                    difficulty_label = "Senior"; difficulty_factor = 1.0
                    modo_juego = "intro"
                    is_practice_mode = False  # No es práctica
                else:  # back
                    modo_juego = "menu"
                # Si pasamos a intro, detener música de menú
                if modo_juego == "intro":
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                    current_music_tag = None
                    # Crear intro topdown
                    introscreen = intro_screen.IntroTopdown()
                else:
                    play_menu_music_if_needed()
                playselect = None

        elif modo_juego == "practice":
            practicemenu.handle_event(event)
            if practicemenu.selected_phase is not None:
                print(f"[DEBUG] Selected phase: {practicemenu.selected_phase}")
                if practicemenu.selected_phase in (1, 2, 3):
                    start_battle(practicemenu.selected_phase)
                    practicemenu = None
                elif practicemenu.selected_phase == "secret_boss":
                    print("[DEBUG] Intentando iniciar Boss2...")
                    try:
                        # Detener musica del menu
                        pygame.mixer.music.stop()
                        current_music_tag = None
                        
                        # Limpiar sprites
                        bullets.empty()
                        all_sprites.empty()
                        all_sprites.add(player)
                        
                        # Crear Boss2
                        from characters.boss2 import Boss2
                        enemy = Boss2(bullets, all_sprites, music_volume=music_volume)
                        all_sprites.add(enemy)
                        
                        # Crear sistema de combate (igual que en start_battle)
                        combate = combat.CombatSystem()
                        
                        # Cambiar a modo batalla y modo practica
                        is_practice_mode = True
                        modo_juego = "batalla"
                        practicemenu = None
                        print(f"[SECRET] Boss2 iniciado, modo_juego={modo_juego}")
                        print(f"[SECRET] enemy type: {type(enemy).__name__}, HP: {enemy.hp}")
                    except Exception as e:
                        import traceback
                        print(f"[WARNING] Error iniciando Boss2: {e}")
                        traceback.print_exc()
                        practicemenu.selected_phase = None
                elif practicemenu.selected_phase == "back":
                    modo_juego = "menu"
                    practicemenu = None
                    play_menu_music_if_needed()

        elif modo_juego == "options":
            result = optsmenu.handle_event(event)
            if result == "back":
                modo_juego = "menu"; optsmenu = None
                play_menu_music_if_needed()

        elif modo_juego == "credits":
            result = creditss.handle_event(event)
            if result == "back":
                modo_juego = "menu"; creditss = None
                play_menu_music_if_needed()

        elif modo_juego == "victoria":
            # Pasar eventos a la pantalla de victoria (no volver a leer eventos más tarde)
            if victoryscreen:
                action = victoryscreen.handle_event(event)
                if action == "menu":
                    # Volver al menú principal
                    bullets.empty()
                    all_sprites.empty()
                    enemy = None
                    combate = None
                    victoryscreen = None
                    modo_juego = "menu"
                    try:
                        current_music_tag = None
                    except Exception:
                        pass
                    play_menu_music_if_needed()
                elif action == "quit":
                    pygame.quit()
                    sys.exit()

        # Intro topdown: delegar eventos
        if modo_juego == "intro" and introscreen:
            result = introscreen.handle_event(event)
            if result == 'start_battle':
                is_practice_mode = False
                start_battle()


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
        # Fondo por defecto para pantallas que no son batalla
        screen.fill((30, 20, 30))

    # --- Intro ---
    if modo_juego == "menu":
        main_menu.update()
        main_menu.draw(screen)
        # Dibujar estrellas animadas debajo del título
        _draw_stars(screen)

    elif modo_juego == "play_select":
        playselect.update(); playselect.draw(screen)

    elif modo_juego == "practice":
        practicemenu.update(); practicemenu.draw(screen)

    elif modo_juego == "options":
        optsmenu.update(); optsmenu.draw(screen)

    elif modo_juego == "credits":
        creditss.update(); creditss.draw(screen)

    elif modo_juego == "intro":
        if introscreen:
            result = introscreen.update()
            introscreen.draw(screen)
            # Check if transition to battle is complete
            if result == 'start_battle':
                is_practice_mode = False
                start_battle()

    # --- Batalla ---
    elif modo_juego == "batalla":
        # DEBUG: Verificar tipo de enemy
        if enemy and not hasattr(enemy, '_debug_printed'):
            print(f"[BATALLA] Enemy type: {type(enemy).__name__}, HP: {enemy.hp}, Phase: {enemy.phase}")
            enemy._debug_printed = True
        
        keys = pygame.key.get_pressed()
        player.update(keys)
        
        # Si el chat está activo, manejar eventos de texto
        if combate and combate.chat_active:
            # No procesar eventos de batalla normales cuando el chat está activo
            pass
        else:
            combate.update(player, enemy)

        # Si el jefe marcó victoria lista, pasar a pantalla de victoria
        if enemy and getattr(enemy, 'victory_ready', False):
            pygame.mixer.music.stop()
            modo_juego = "victoria"
            bullets.empty()
            # Crear pantalla de victoria con estadísticas
            victoryscreen = victory_screen.VictoryScreen(
                difficulty_label=difficulty_label,
                intentos=intentos,
                is_practice=is_practice_mode
            )

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
                # Flash y transiciones solo para el boss original
                if hasattr(enemy, 'draw_flash_effect'):
                    enemy.draw_flash_effect(screen)
                if hasattr(enemy, 'check_phase3_transition'):
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
                # Flash y transiciones solo para el boss original
                if hasattr(enemy, 'draw_flash_effect'):
                    enemy.draw_flash_effect(screen)
                if hasattr(enemy, 'check_phase3_transition'):
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
                # Transición de fase 3 solo para boss original
                if hasattr(enemy, 'check_phase3_transition'):
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
                # Flash solo para boss original
                if hasattr(enemy, 'draw_flash_effect'):
                    enemy.draw_flash_effect(screen)
                _draw_tutorial_hint(screen, enemy)

            if player.hp <= 0:
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load("Juego/assets/Soundtrack/GameOver.mp3")
                    pygame.mixer.music.set_volume(music_volume)
                    pygame.mixer.music.play(0)
                except Exception as e:
                    print("Error al reproducir GameOver:", e)
                go_to_menu = gameover.game_over_screen(screen, clock)
                if go_to_menu:
                    # Volver al menú principal
                    bullets.empty()
                    all_sprites.empty()
                    enemy = None
                    combate = None
                    modo_juego = "menu"
                    intentos += 1
                    try:
                        current_music_tag = None
                    except Exception:
                        pass
                    play_menu_music_if_needed()
                else:
                    # Reintentar (Space)
                    reset_game()

    elif modo_juego == "victoria":
        # Eventos ya manejados en el bucle principal; aquí solo lógicas y render
        # Otorgar estrella si no es modo práctica
        if not is_practice_mode:
            if difficulty_label == "Junior" and not stars_junior:
                stars_junior = True
                print("[STAR] ¡Estrella Junior desbloqueada!")
            elif difficulty_label == "Senior" and not stars_senior:
                stars_senior = True
                print("[STAR] ¡Estrella Senior desbloqueada!")
            # Actualizar música si ahora tiene ambas
            if stars_junior and stars_senior:
                try:
                    current_music_tag = None
                except Exception:
                    pass
        
        # Actualizar y renderizar pantalla de victoria
        if victoryscreen:
            victoryscreen.update()
            victoryscreen.draw(screen)

    # --- Contador de intentos (solo durante la batalla) ---
    if modo_juego == "batalla" and intentos > 0:
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
