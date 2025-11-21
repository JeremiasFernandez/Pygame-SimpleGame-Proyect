import os, sys
import pygame, random, math

# Permitir ejecutar este archivo directamente arreglando sys.path para que 'Const' se resuelva
_this_file = os.path.abspath(__file__)
_codigo_dir = os.path.dirname(os.path.dirname(_this_file))  # .../Codigo
if _codigo_dir not in sys.path:
    sys.path.insert(0, _codigo_dir)

import Const as c
from characters.bullet import Bullet, AttackManager

# Si este archivo se ejecuta directamente, informar cómo ejecutar el juego correctamente
if __name__ == "__main__":
    print("Este archivo define la clase Boss. Para jugar, ejecuta Juego/Codigo/main.py")
    print("Ejemplo (PowerShell): cd Juego/Codigo; python .\\main.py")
    # Inicializar pygame solo para mostrar mensaje de versión (ya imprime en algunos entornos)
    try:
        import pygame
        pygame.init()
    except Exception:
        pass
class Boss(pygame.sprite.Sprite):
    def __init__(self, bullets_group, all_sprites, music_volume=0.5):
        super().__init__()
        # Inicialización de grupos
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites
        self.attack_manager = AttackManager(self, bullets_group, all_sprites)
        print("🎯 Boss creado con grupos:", len(bullets_group), "balas,", len(all_sprites), "sprites")

        self.timer = 0
        self.attack_timer = 0
        self.attack_duration = 420 # 18 segundos
        self.hp = 200
        self.phase = 1
        self.difficulty = 1.0
        self.music_volume = music_volume  # Guardar volumen de música para transiciones de fase
        self.current_attack = None
        self._first_attack_forced = False
        self.music_playing = False
        self._phase2_entered = False
        self.phase2_music_started = False

        try:
            img1 = pygame.image.load("Juego/assets/sprites/Boss_Virus_1.png").convert_alpha()
        except:
            img1 = pygame.Surface((200, 200), pygame.SRCALPHA); img1.fill((220,220,220,255))
        self.image = pygame.transform.scale(img1, (200, 200))
        self.rect = self.image.get_rect()

        # --- POSICIONAMIENTO ---
        # Usar modo 'anchor' para que el jefe SIEMPRE quede estático en la misma posición
        # sin depender del tamaño del sprite ni animaciones.
        self.pos_mode = "anchor"  # "absolute" usa pos_abs; "anchor" usa self.positioning
        self.pos_abs = {
            1: (c.ANCHO // 2, (c.BOX_Y - 12) - self.rect.height // 2),  # default: igual que antes, pero como centro
            2: (c.ANCHO // 2, (c.BOX_Y - 12) - self.rect.height // 2),
            3: (c.ANCHO // 2, (c.BOX_Y - 12) - self.rect.height // 2),
            "defeated": (400, 160),
        }

        # --- Posicionamiento manual por fase ---
        # Cambia estas posiciones a gusto. Anchor puede ser: "midbottom", "center" o "topleft".
        self.positioning = {
               1: (400, 140),        # Fase 1: centro en (x=400, y=140)
               2: (400, 140),        # Fase 2: centro
               3: (400, 140),        # Fase 3: centro
               "defeated": (400, 160) # Derrotado: centro
        }

        # Aplicar posición para fase 1 (anchor midbottom, siempre igual)
        self.apply_position(1)

        try:
            img2 = pygame.image.load("Juego/assets/sprites/Boss_Virus_2.png").convert_alpha()
            self._phase2_img = pygame.transform.scale(img2, (300, 300))
        except:
            self._phase2_img = None

        self.dialogo = None
        self.dialogo_timer = 0
        self.silencio_activo = False  # ✅ ESTA LÍNEA AGREGA EL CONTROL DE SILENCIO
        self._fase3_silence_duration = 4500  # milisegundos: ~4.5s de silencio antes de la activación de fase 3
        self.puede_ser_atacado = True
        self.font = pygame.font.Font(None, 28)

        # Ataques por fase
        self.phase1_attacks = ["attack_tutorial", "attack_rain", "attack_diagonal", "attack_lateral1", "attack_lateral2", "attack_burst1", "attack_burst3"]
        self.phase2_attacks = ["attack_spears", "attack_spearstorm"]  # Fase 2 solo usa ataques de lanzas
        # Ataques más intensos (fase 3)
        self.phase3_attacks = [
            "attack_spears",
            "attack_spearstorm",
            "attack_spearain",
            "attack_spearwaves",
            "attack_spearcross",
            "attack_ballscircle",
        ]

        # Variables de animación y efectos visuales
        self.phase2_red_base = (54, 0, 0)
        self.flash_alpha = 0  # Para el efecto de destello blanco
        self.bg_color = (0, 0, 0)  # Color de fondo dinámico
        self.movement_timer = 0  # Para movimiento lateral
        self.movement_direction = 1  # 1 derecha, -1 izquierda
        self.original_x = self.rect.centerx  # Posición original para movimiento
        self.phase3_colors = [(255,128,0), (255,0,0), (255,255,0)]  # Colores estilo Asgore
        self.particles = []
        self.move_amplitude = 0  # Desactivar movimiento lateral por defecto

    def apply_position(self, key):
        """Aplica la posición del jefe para la clave dada (1,2,3,"defeated").

        Soporta dos formatos en self.positioning:
        - Dict por fase: { 'anchor': 'midbottom'|'center'|'topleft', 'pos': (x,y) }
        - Tupla (x, y) directa: se interpreta como centro (anchor='center')
        """
        # Modo absoluto: usa coordenadas exactas (centro)
        if getattr(self, "pos_mode", "anchor") == "absolute":
            pos = self.pos_abs.get(key)
            if pos is None:
                # Fallback: reproducir la posición clásica de estar justo encima del border con margin=12
                cx = c.ANCHO // 2
                cy = (c.BOX_Y - 12) - self.rect.height // 2
                pos = (cx, cy)
            self.rect.center = (int(pos[0]), int(pos[1]))
            return

        # Modo anchor (alternativa) con soporte de tuplas simples
        cfg = self.positioning.get(key)
        if cfg is None:
            return

        # Si el usuario puso directamente una tupla/lista (x,y), interpretamos como center
        if isinstance(cfg, (tuple, list)) and len(cfg) == 2:
            x, y = int(cfg[0]), int(cfg[1])
            self.rect.center = (x, y)
            return

        # Si es dict, usar anchor + pos
        if isinstance(cfg, dict):
            anchor = cfg.get("anchor", "midbottom")
            x, y = cfg.get("pos", (c.ANCHO // 2, c.BOX_Y - 12))
            if anchor == "center":
                self.rect.center = (x, y)
            elif anchor == "topleft":
                self.rect.topleft = (x, y)
            else:  # midbottom por defecto
                self.rect.midbottom = (x, y)
            return

        # Formato no reconocido: no mover
        return

    def set_pos(self, phase_key, x, y):
        """Define posición absoluta (centro) para una fase y la aplica si corresponde."""
        if not hasattr(self, "pos_abs"):
            self.pos_abs = {}
        self.pos_abs[phase_key] = (int(x), int(y))
        # Si es la fase actual (o defeated activo), aplicar inmediatamente
        if (phase_key == self.phase) or (phase_key == "defeated" and getattr(self, "_muerte_final", False)):
            self.rect.center = (int(x), int(y))

    def update(self):
        """Actualiza el estado del jefe."""
        # Asegurar SIEMPRE la misma posición del jefe sin importar el modo de entrada
        # Re-ancla cada frame usando el esquema 'anchor' para la fase actual (o estado derrotado)
        try:
            if getattr(self, "_muerte_final", False):
                self.apply_position("defeated")
            else:
                self.apply_position(self.phase)
        except Exception:
            # Ante cualquier inconveniente, no interrumpir el update
            pass

        # Si ya murió definitivamente, esperar unos segundos y marcar victoria
        if getattr(self, "_muerte_final", False):
            # Inicializar temporizador de victoria si no existe
            if not hasattr(self, "_victory_timer"):
                self._victory_timer = 180  # ~3s a 60 FPS
                self.victory_ready = False
            # Decrementar timer
            if self._victory_timer > 0:
                self._victory_timer -= 1
                if self._victory_timer == 0:
                    self.victory_ready = True
            return

        self.timer += 1
        
        # Control de diálogo
        if self.dialogo_timer > 0:
            self.dialogo_timer -= 1
            if self.dialogo_timer == 0:
                self.dialogo = ""

        # Actualizar efecto de titileo del spearcross
        if hasattr(self.attack_manager, 'update_spearcross_flash'):
            self.attack_manager.update_spearcross_flash()

        # --- PHASE 1 & 2: select and execute attacks normally (unless silence active)
        if self.phase in (1, 2) and not self.silencio_activo:
            # decrement attack timer if running
            if self.attack_timer > 0:
                self.attack_timer -= 1

            # choose a new attack if none or timer expired
            if not self.current_attack or self.attack_timer <= 0:
                self.cambiar_ataque()

            # execute current attack (attacks are usually time/mod based inside)
            if self.current_attack:
                try:
                    attack_method = getattr(self.attack_manager, self.current_attack)
                    attack_method(self.timer, self.difficulty)
                except AttributeError:
                    print(f"[WARNING] Ataque no implementado: {self.current_attack}")
                    self.current_attack = None
                    self.attack_timer = 60
                except Exception as e:
                    print(f"❌ Error ejecutando ataque: {e}")
                    self.cambiar_ataque()

            # after handling phase1/2 attacks, return to avoid phase3 handling below
            return

        # Actualizar efectos visuales de fase 3
        if self.phase == 3:
            # Efecto de destello blanco con fadeout
            if hasattr(self, '_flash_fadeout') and self._flash_fadeout and self.flash_alpha > 0:
                self.flash_alpha = max(0, self.flash_alpha - 8)  # Velocidad del fadeout
                if self.flash_alpha == 0:
                    self._flash_fadeout = False

            # Si no hay ataque actual o el timer llegó a 0, elegir nuevo ataque
            if not self.current_attack or self.attack_timer <= 0:
                self.cambiar_ataque()
                self.attack_timer = 120
            
            # Ejecutar el ataque actual
            if self.current_attack:
                try:
                    attack_method = getattr(self.attack_manager, self.current_attack)
                    attack_method(self.timer, self.difficulty)
                    self.attack_timer = max(0, self.attack_timer - 1)  # Decrementar el timer
                except Exception as e:
                    print(f"❌ Error ejecutando ataque: {e}")
                    self.cambiar_ataque()  # Intentar otro ataque si falla
            # Actualizar timer
            if self.attack_timer > 0:
                self.attack_timer -= 1
                return  # No hacer nada más si el timer está activo
            
            # Si no hay ataque actual o el timer llegó a 0, elegir nuevo ataque
            if not self.current_attack or self.attack_timer <= 0:
                self.cambiar_ataque()  # Esto seleccionará un nuevo ataque y reiniciará el timer
                if self.current_attack:
                    print(f"🎯 Nuevo ataque iniciado: {self.current_attack}")
                    # Ejecutar el ataque actual una sola vez
                    try:
                        attack_method = getattr(self.attack_manager, self.current_attack)
                        attack_method(self.timer, self.difficulty)
                        self.attack_timer = 120  # Reiniciar el timer después del ataque
                    except AttributeError:
                        print(f"[WARNING] Ataque no implementado: {self.current_attack}")
                        self.current_attack = None
                    except Exception as e:
                        print(f"❌ Error ejecutando ataque: {e}")
        elif self.silencio_activo:
            print("🔇 Silencio activo - sin ataques")

    def _select_and_execute_attack(self):
        """Selecciona y ejecuta un ataque basado en la fase actual."""
        try:
            # Verificar si es tiempo de cambiar de ataque
            if not self.current_attack or self.attack_timer <= 0:
                self.cambiar_ataque()
            
            # Ejecutar el ataque actual
            if self.attack_manager and self.current_attack:
                try:
                    # Intentar ejecutar el ataque directamente
                    attack_method = getattr(self.attack_manager, self.current_attack)
                    attack_method(self.timer, self.difficulty)
                except AttributeError as e:
                    print(f"[WARNING] Ataque no implementado: {self.current_attack}")
                    self.current_attack = None
                    self.attack_timer = 60
                except Exception as e:
                    print(f"❌ Error ejecutando ataque {self.current_attack}:", e)
        except Exception as e:
            print("❌ Error general en _select_and_execute_attack:", e)
            print(f"[WARNING] Ataque no implementado: {self.current_attack}")
            self.current_attack = None
            self.attack_timer = 60

    def check_phase3_transition(self):
        """Maneja la transición a fase 3 cuando el jefe es derrotado en fase 2."""
        # Fase 3: transición cuando hp llega a 0 en fase 2
        if self.phase == 2 and self.hp <= 0 and not hasattr(self, "_fase3_iniciada"):
            print("⚡ Iniciando transición a fase 3...")
            self._fase3_iniciada = True
            self._fase3_tiempo_muerte = pygame.time.get_ticks()
            try:
                # Cambiar sprite y detener música
                self.image = pygame.image.load("Juego/assets/Sprites/boss_derrotado.png").convert_alpha()
                self.image = pygame.transform.scale(self.image, (300, 300))
                self.rect = self.image.get_rect()
                # Aplicar posicionamiento manual para 'defeated'
                self.apply_position("defeated")
                
                # Detener música actual y reproducir silencio
                pygame.mixer.music.stop()
                try:
                    self.silence_sound = pygame.mixer.Sound("Juego/assets/Sounds/silence.wav")
                    self.silence_sound.set_volume(0.4)
                    self.silence_sound.play()
                except Exception as e:
                    print(f"❌ Error cargando silence.wav: {e}")
                
                # Activar silencio y limpiar efectos
                self.silencio_activo = True
                self.current_attack = None
                self.phase2_music_started = False
                
                # Limpiar partículas y balas
                self.attack_manager.clear_attacks()
                if hasattr(self, 'particles'):
                    self.particles.clear()
                
                # Configurar estado
                self.puede_ser_atacado = False
                self.dialogo = "..."
                self.dialogo_timer = 300
                
                print(f"🔇 Fase 3: Silencio iniciado (esperando {self._fase3_silence_duration/1000} segundos)")
            except Exception as e:
                print("❌ Error iniciando transición fase 3:", e)

        # Verificar si debemos activar fase 3
        if hasattr(self, "_fase3_tiempo_muerte") and not hasattr(self, "_fase3_activada"):
            tiempo_actual = pygame.time.get_ticks()
            tiempo_espera = tiempo_actual - self._fase3_tiempo_muerte
            
            if tiempo_espera >= self._fase3_silence_duration:
                print(f"⏰ Tiempo de espera completado ({tiempo_espera/1000} segundos)")
                try:
                    self._activar_fase3()
                except Exception as e:
                    print("❌ Error activando fase 3:", e)

    def _enter_phase2(self):
        if self._phase2_entered:
            return
            
        # Limpiar ataques actuales
        self.attack_manager.clear_attacks()
        self.current_attack = None
        
        # Cambiar estado de fase
        self._phase2_entered = True
        self.phase = 2
        
        # Cambiar sprite
        center = self.rect.center
        if self._phase2_img:
            self.image = self._phase2_img
        else:
            surf = pygame.Surface((200,200), pygame.SRCALPHA)
            surf.fill((180, 60, 60, 255))
            self.image = surf
        self.rect = self.image.get_rect(center=center)
        # Posicionar según configuración manual para fase 2
        self.apply_position(2)
        # Reanclar posición base horizontal para movimiento lateral en fase 2
        self.original_x = self.rect.centerx
        
        # Ajustar dificultad y estado
        self.difficulty = 1.3
        self.attack_timer = 0
        self.phase2_music_started = False
        
        # Mensaje
        self.decir("¡TE MOSTRARÉ MI VERDADERA FORMA!")
        print("🎯 Fase 2 iniciada con dificultad:", self.difficulty)

    def cambiar_ataque(self):
        """Cambia el ataque actual basado en la fase."""
        try:
            # Forzar que el PRIMER ataque de la fase 1 sea el tutorial
            if self.phase == 1 and not getattr(self, "_first_attack_forced", False):
                self.current_attack = "attack_tutorial"
                self._first_attack_forced = True
                self.attack_timer = 120
                self.decir("¡EMPEZAMOS! (Tutorial)")
                print("🎓 Primer ataque forzado: attack_tutorial")
                return

            # Determinar pool de ataques basado en la fase
            if self.phase == 1:
                ataques = self.phase1_attacks
            elif self.phase == 2:
                ataques = self.phase2_attacks
            else:  # fase 3
                ataques = self.phase3_attacks

            # Evitar repetir el mismo ataque
            posibles = [a for a in ataques if a != self.current_attack]
            if not posibles:  # si no hay otros ataques, usar todos
                posibles = ataques
            self.current_attack = random.choice(posibles)
            
            if self.phase == 3:
                self.decir("¡SIENTE MI PODER FINAL!")
            else:
                self.decir(f"¡MI ATAQUE {self.current_attack.upper()} TE ANIQUILARÁ!")
            
            # Reiniciar timer
            self.attack_timer = 120
            
            print(f"🎯 Nuevo ataque seleccionado: {self.current_attack}")
        except Exception as e:
            print(f"❌ Error cambiando ataque: {e}")
            self.current_attack = self.phase1_attacks[0]  # Fallback a ataque básico

    def phase_one_behavior(self):
        """Comportamiento específico de fase 1"""
        if self.current_attack:
            try:
                attack_method = getattr(self.attack_manager, self.current_attack)
                attack_method(self.timer, self.difficulty)
            except Exception as e:
                print(f"❌ Error en fase 1: {e}")
                self.cambiar_ataque()  # Cambiar a otro ataque si falla

    def phase_two_behavior(self):
        """Comportamiento específico de fase 2 - Más agresivo"""
        if self.current_attack:
            try:
                attack_method = getattr(self.attack_manager, self.current_attack)
                attack_method(self.timer, self.difficulty)
            except Exception as e:
                print(f"❌ Error en fase 2: {e}")
                self.cambiar_ataque()  # Cambiar a otro ataque si falla

    def draw_health_bar(self, screen):
        vida_max = 200
        vida_actual = max(0, self.hp)
        barra_ancho, barra_alto = 250, 15
        barra_x = (c.ANCHO // 2) - (barra_ancho // 2)
        barra_y = 30
        propor = vida_actual / vida_max
        relleno = int(barra_ancho * propor)
        pygame.draw.rect(screen, c.GRIS,  (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(screen, c.ROJO,  (barra_x, barra_y, relleno,     barra_alto))
        pygame.draw.rect(screen, c.BLANCO,(barra_x, barra_y, barra_ancho, barra_alto), 2)
        f = pygame.font.Font(None, 28)
        t = f.render(f"{vida_actual}/{vida_max}", True, c.BLANCO)
        screen.blit(t, t.get_rect(center=(c.ANCHO // 2, barra_y + barra_alto // 2)))

    def decir(self, texto, duracion=150):
        self.dialogo = texto
        self.dialogo_timer = duracion

    def draw_flash_effect(self, screen):
        """Dibuja el efecto de flash blanco (separado del diálogo)."""
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((c.ANCHO, c.ALTO))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(self.flash_alpha)
            screen.blit(flash_surface, (0, 0))

    def draw_cross_indicator(self, screen):
        """Dibuja el indicador de warning del spearcross."""
        if hasattr(self.attack_manager, 'draw_spearcross_flash'):
            self.attack_manager.draw_spearcross_flash(screen)

    def draw_dialogue(self, screen):
        # Dibujar efectos visuales de fase 3
        if self.phase == 3:
            # Color de fondo dinámico
            bg_surface = pygame.Surface((c.ANCHO, c.ALTO))
            bg_surface.fill(self.bg_color)
            screen.blit(bg_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
            
            # Efecto de destello blanco
            self.draw_flash_effect(screen)

        # Dibujar el diálogo
        if not self.dialogo: return
        text_surf = self.font.render(self.dialogo, True, c.BLANCO)
        rect = text_surf.get_rect(center=(c.ANCHO // 2, self.rect.bottom + 30))
        screen.blit(text_surf, rect)

    def draw_phase2_background(self, screen):
        if self.silencio_activo:
            screen.fill((0, 0, 0))
            self.particles = []
            return
        if self.phase != 2:
            return
        base = pygame.Surface((c.ANCHO, c.ALTO), pygame.SRCALPHA)
        base.fill((*self.phase2_red_base, 230))
        screen.blit(base, (0, 0))
        if random.random() < 0.25:
            while True:
                x = random.randint(0, c.ANCHO)
                y = random.randint(0, c.ALTO)
                if not (c.BOX_X < x < c.BOX_X + c.BOX_ANCHO and c.BOX_Y < y < c.BOX_Y + c.BOX_ALTO):
                    break
            dx = random.uniform(-0.4, 0.4)
            dy = random.uniform(-1.0, -0.3)
            size = random.randint(1, 2)
            life = random.randint(60, 120)
            color = (255, 230, 120)
            self.particles.append([x, y, dx, dy, size, life, color])
        alive = []
        for (x, y, dx, dy, size, life, color) in self.particles:
            x += dx; y += dy; life -= 1
            if life > 0:
                alpha = max(0, min(180, life + 60))
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, alpha), (size, size), size)
                screen.blit(s, (x, y))
                alive.append([x, y, dx, dy, size, life, color])
        self.particles = alive


    def draw_phase3_background(self, screen):
        """Dibuja fondo y partículas para fase 3 (muchas más que fase 2)."""
        if self.phase != 3:
            return
        
        # Spawn de muchas más partículas (probabilidad más alta y más cantidad)
        if random.random() < 0.6:  # Era 0.25 en fase 2, ahora 0.6
            num_particles = random.randint(2, 4)  # Spawn múltiples partículas a la vez
            for _ in range(num_particles):
                while True:
                    x = random.randint(0, c.ANCHO)
                    y = random.randint(0, c.ALTO)
                    # Evitar spawneo dentro del border
                    if not (c.BOX_X < x < c.BOX_X + c.BOX_ANCHO and c.BOX_Y < y < c.BOX_Y + c.BOX_ALTO):
                        break
                dx = random.uniform(-0.5, 0.5)
                dy = random.uniform(-1.2, -0.4)
                size = random.randint(1, 3)  # Tamaños variados
                life = random.randint(80, 150)  # Vida más larga
                # Colores variados para fase 3 (naranja, amarillo, rojo)
                color = random.choice([(255, 200, 0), (255, 128, 0), (255, 100, 50)])
                self.particles.append([x, y, dx, dy, size, life, color])
        
        # Renderizar partículas
        alive = []
        for (x, y, dx, dy, size, life, color) in self.particles:
            x += dx
            y += dy
            life -= 1
            if life > 0:
                alpha = max(0, min(200, life + 80))
                s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, alpha), (size, size), size)
                screen.blit(s, (x, y))
                alive.append([x, y, dx, dy, size, life, color])
        self.particles = alive


    def _activar_fase3(self):
        """Activa la fase 3 del jefe después del período de silencio."""
        print("🎯 Activando fase 3...")
        try:
            # 1. Detener silence.wav si está sonando
            if hasattr(self, 'silence_sound') and self.silence_sound:
                print("🔇 Deteniendo silence.wav...")
                self.silence_sound.stop()
                pygame.mixer.stop()  # Detener TODOS los efectos de sonido
                del self.silence_sound

            # 2. Efecto de destello blanco + flash sound
            self.flash_alpha = 255  # Pantalla completamente blanca
            try:
                # Cargar y reproducir flash.wav INMEDIATAMENTE
                flash_sound = pygame.mixer.Sound("Juego/assets/Sounds/flash.wav")
                flash_sound.set_volume(1.0)  # Volumen máximo
                channel = flash_sound.play()
                if channel:
                    print("🔊 flash.wav reproduciendo correctamente")
                else:
                    print("❌ No se pudo reproducir flash.wav - no hay canales disponibles")
            except FileNotFoundError:
                print(f"❌ Error: No se encuentra Juego/assets/Sounds/flash.wav")
            except Exception as e:
                print(f"❌ Error cargando flash.wav: {e}")

            # 3. Cargar sprite y posicionarlo IGUAL que fase 1
            img = pygame.image.load("Juego/assets/Sprites/Boss_Virus_3.png").convert_alpha()
            self.image = pygame.transform.scale(img, (233, 350))
            self.rect = self.image.get_rect()
            # Posicionar según configuración manual para fase 3
            self.apply_position(3)
            self.original_x = self.rect.centerx
            
            # 4. Cambiar música
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Juego/assets/Soundtrack/phase3.mp3")
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)

            # Iniciar el fadeout del destello
            self._flash_fadeout = True
            
            # 4. Restaurar vida y configurar fase 3
            self.phase = 3
            self.hp = 70  # Resucita con 70 HP (antes era 50)
            self.difficulty = 1.6
            self.attack_timer = 0
            self.current_attack = random.choice(self.phase3_attacks)
            
            # 5. Reactivar comportamiento normal
            self.puede_ser_atacado = True
            self.silencio_activo = False
            
            # 6. Diálogo y estado
            self.dialogo = "¡ESTA ES MI FORMA FINAL!"
            self.dialogo_timer = 300
            self._fase3_activada = True
            
            print(f"🧬 Fase 3 activada exitosamente (HP: {self.hp})")
        except Exception as e:
            print("❌ Error activando fase 3:", e)
            # Intentar recuperarse del error
            self.phase = 3
            self.hp = 70
            self.puede_ser_atacado = True
            self.silencio_activo = False
            
    def hit(self, damage=10):
        """El jefe recibe daño y maneja las transiciones de fase.

        Accepts an optional damage amount (default 10). This lets callers
        use enemy.hit(100) for debug or enemy.hit() for standard attacks.
        """
        if not self.puede_ser_atacado:
            return

        # Reducir HP por la cantidad indicada
        self.hp -= damage
        print(f"💥 Boss dañado (HP: {self.hp})")

        # Verificar transiciones
        if self.phase == 1 and self.hp <= 100:
            print("🔄 Transición a fase 2")
            self._enter_phase2()
            # Asegurar HP positivo al entrar a fase 2 (evita estados atascados si cayó a <= 0)
            if self.hp <= 0:
                self.hp = 50
            
            # Cargar música de fase 2 si aún no está cargada
            if not self.phase2_music_started:
                try:
                    pygame.mixer.music.load("Juego/assets/Soundtrack/phase2.mp3")
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)
                    self.phase2_music_started = True
                    print("[MUSIC] Musica de fase 2 iniciada")
                except Exception as e:
                    print(f"[WARNING] Error cargando musica fase 2: {e}")
                    
        elif self.phase == 2 and self.hp <= 0:
            print("🔄 Iniciando transición a fase 3")
            self.check_phase3_transition()
            # Limpiar ataques y partículas
            self.attack_manager.clear_attacks()
            if hasattr(self, 'particles'):
                self.particles.clear()
            
        elif self.phase == 3 and self.hp <= 0:
            print("💀 Muerte definitiva")
            self._muerte_definitiva()
            
    def _muerte_definitiva(self):
        """El jefe muere definitivamente al perder toda su vida en fase 3."""
        try:
            # Detener música y ataques
            pygame.mixer.music.stop()
            self.attack_manager.clear_attacks()
            self.current_attack = None
            self.puede_ser_atacado = False
            
            # Cambiar sprite a versión derrotada/muerta
            try:
                img = pygame.image.load("Juego/assets/Sprites/boss_derrotado.png").convert_alpha()
                self.image = pygame.transform.scale(img, (300, 300))
                self.rect = self.image.get_rect()
                # Usar posicionamiento manual (absolute/anchor según configuración)
                self.apply_position("defeated")
            except:
                # Si no hay sprite de muerte, oscurecer el actual
                self.image.fill((40, 40, 40, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Marcar como definitivamente muerto
            self._muerte_final = True
            self.dialogo = "¡NOOOOOO! ¡IMPOSIBLE!"
            self.dialogo_timer = 300
            
            print("💀 ¡Jefe definitivamente derrotado!")
        except Exception as e:
            print("❌ Error en muerte definitiva:", e)
