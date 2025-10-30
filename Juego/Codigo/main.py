import pygame, random, sys
import Const as c
import characters.player as p
import characters.bullet as bullet
import characters.boss as boss
import screens.gameover as gameover
from characters.border import Border
import screens.combat as combat

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
combate = combat.CombatSystem()  # crear el sistema de combate


# --- Variables globales ---
enemy = None
modo_juego = "intro"
font = pygame.font.Font(None, 36)
border = Border()
combate = combat.CombatSystem()  # 👈 Sistema de combate

# --- Función para mostrar texto centrado ---
def mostrar_texto(texto, color, y):
    render = font.render(texto, True, color)
    rect = render.get_rect(center=(c.ANCHO // 2, y))
    screen.blit(render, rect)

# --- Reiniciar juego ---
def reset_game():
    global bullets, player, enemy, modo_juego, combate
    bullets.empty()
    all_sprites.empty()

    player = p.Player()
    enemy = boss.Boss(bullets, all_sprites)
    all_sprites.add(player)
    all_sprites.add(enemy)

    combate = combat.CombatSystem()  # 👈 reset combate
    modo_juego = "batalla"

# --- Bucle principal ---
running = True
while running:
    clock.tick(c.FPS)

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if modo_juego == "intro" and event.key == pygame.K_x:
                modo_juego = "batalla"
                enemy = boss.Boss(bullets, all_sprites)
                all_sprites.add(enemy)
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Juego/assets/Soundtrack/phase1.mp3")
                    pygame.mixer.music.set_volume(0.6)
                    pygame.mixer.music.play(-1)
                except:
                    print("⚠️ No se pudo cargar la música de fase 1.")

    # --- Lógica según modo ---
    if modo_juego == "intro":
        screen.fill((10, 10, 20))
        mostrar_texto("Tu computadora tiene un VIRUS...", c.ROJO, c.ALTO // 2 - 50)
        mostrar_texto("Presiona [X] para enfrentarlo", c.BLANCO, c.ALTO // 2 + 20)

    elif modo_juego == "batalla":
        keys = pygame.key.get_pressed()
        player.update(keys)

        # --- Actualizar combate (menu / ataque / defensa) ---
        combate.update(player, enemy)


        screen.fill(c.NEGRO)
        border.draw(screen)

        # --- Solo dibuja el boss cuando no estás en el menú ---
        if combate.state != "menu":
            all_sprites.draw(screen)
            border.draw(screen)
            player.draw_health_bar(screen)

        if enemy:
            enemy.draw_dialogue(screen)

        # --- Menú o mensajes ---
        combate.draw(screen)
        pygame.display.flip()


        # --- Si está en defensa, también se mueven las balas ---
        if combate.state == "defensa":
            bullets.update()
            if enemy:
                enemy.update()
            border.update(player)

            # colisiones con balas
            hits = pygame.sprite.spritecollide(player, bullets, True)
            for hit in hits:
                player.take_damage(5)

        # --- Dibujar ---
        screen.fill(c.NEGRO)
        border.draw(screen)
        all_sprites.draw(screen)
        if enemy:
            enemy.draw_dialogue(screen)
        player.draw_health_bar(screen)
        combate.draw(screen)  # 👈 interfaz del combate

        # --- Si el jugador muere ---
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

    # --- Actualizar pantalla ---
    pygame.display.flip()

pygame.quit()
sys.exit()
