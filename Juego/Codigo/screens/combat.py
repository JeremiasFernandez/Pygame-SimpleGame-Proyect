import pygame
import random
import Const as c
import os
import threading

class AttackEffect(pygame.sprite.Sprite):
    def __init__(self, enemy_rect):
        super().__init__()
        self.frames = []
        slash_path = os.path.join("Juego", "assets", "Sprites", "slash.gif")
        self.load_frames_from_gif(slash_path)
        if not self.frames:
            # Fallback si no se pudo cargar el GIF
            self.frames = [self._create_fallback_frame()]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=enemy_rect.center)
        self.timer = 0
        self.frame_duration = 6
        self.finished = False

    def load_frames_from_gif(self, path):
        """Carga frames de un GIF animado usando Pillow."""
        try:
            from PIL import Image
            gif = Image.open(path)
            try:
                while True:
                    frame = gif.convert("RGBA")
                    # Escalar a 200x200
                    frame = frame.resize((40, 200), Image.Resampling.LANCZOS)
                    # Convertir PIL a Pygame
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    py_img = pygame.image.fromstring(data, size, mode)
                    self.frames.append(py_img)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            print(f"⚔️ Slash GIF cargado: {len(self.frames)} frames")
        except ImportError:
            print("⚠️ PIL/Pillow no disponible para slash.gif, usando fallback")
        except Exception as e:
            print(f"⚠️ Error cargando slash.gif: {e}, usando fallback")

    def _create_fallback_frame(self):
        """Crea un frame de respaldo si el GIF no se pudo cargar."""
        surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        # Dibujar una X simple
        pygame.draw.line(surf, (255, 100, 100), (40, 40), (160, 160), 8)
        pygame.draw.line(surf, (255, 100, 100), (160, 40), (40, 160), 8)
        return surf

    def update(self):
        self.timer += 1
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True
            else:
                self.image = self.frames[self.current_frame]


class CombatSystem:
    def __init__(self):
        self.state = "menu"
        # Volver a la fuente por defecto usada antes
        self.font = pygame.font.Font(None, 36)
        self.selected = 0
        self.timer = 0
        self.DEFENSA_DUR = int(10 * 60)

        self._x_prev = False
        self._left_prev = False
        self._right_prev = False

        try:
            self.attack_sound = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "Attack.wav"))
            self.attack_sound.set_volume(0.5)
        except Exception as e:
            self.attack_sound = None
            print(f"❌ No se pudo cargar Attack.wav: {e}")

        try:
            self.curarse_sound = pygame.mixer.Sound(os.path.join("Juego", "assets", "Sounds", "healup.mp3"))
            self.curarse_sound.set_volume(0.2)
        except Exception as e:
            self.curarse_sound = None
            print(f"❌ No se pudo cargar healup.mp3: {e}")

        self.attack_effect = None
        self.enemy_shake_timer = 0
        self.enemy_base_pos = None

        # --- Barra de tiempo de defensa ---
        self.defense_bar_height = 4  # línea delgada
        self.defense_bar_margin = 8  # píxeles por encima del border
        self.defense_bar_bg = (40, 40, 60, 160)  # fondo semi-transparente
        self.defense_bar_fg = (232, 232, 232)      # color de la barra (restante)

        # --- Sprites para botones de menú (50x23) ---
        self.atacar_normal = None
        self.atacar_selected = None
        self.curarse_normal = None
        self.curarse_selected = None
        
        try:
            atacar_n_path = os.path.join("Juego", "assets", "Sprites", "atacar_normal.png")
            self.atacar_normal = pygame.image.load(atacar_n_path).convert_alpha()
            self.atacar_normal = pygame.transform.scale(self.atacar_normal, (100, 46))
            print(f"✅ Sprite atacar_normal cargado: {atacar_n_path}")
        except Exception:
            print("ℹ️  atacar_normal.png no encontrado; usando texto")
        
        try:
            atacar_s_path = os.path.join("Juego", "assets", "Sprites", "atacar_selected.png")
            self.atacar_selected = pygame.image.load(atacar_s_path).convert_alpha()
            self.atacar_selected = pygame.transform.scale(self.atacar_selected, (100, 46))
            print(f"✅ Sprite atacar_selected cargado: {atacar_s_path}")
        except Exception:
            print("ℹ️  atacar_selected.png no encontrado; usando texto")
        
        try:
            curarse_n_path = os.path.join("Juego", "assets", "Sprites", "curarse_normal.png")
            self.curarse_normal = pygame.image.load(curarse_n_path).convert_alpha()
            self.curarse_normal = pygame.transform.scale(self.curarse_normal, (100, 46))
            print(f"✅ Sprite curarse_normal cargado: {curarse_n_path}")
        except Exception:
            print("ℹ️  curarse_normal.png no encontrado; usando texto")
        
        try:
            curarse_s_path = os.path.join("Juego", "assets", "Sprites", "curarse_selected.png")
            self.curarse_selected = pygame.image.load(curarse_s_path).convert_alpha()
            self.curarse_selected = pygame.transform.scale(self.curarse_selected, (100, 46))
            print(f"✅ Sprite curarse_selected cargado: {curarse_s_path}")
        except Exception:
            print("ℹ️  curarse_selected.png no encontrado; usando texto")

        # --- Diálogos de menú ---
        # Agrega aquí todos los textos que quieras que aparezcan aleatoriamente al entrar al menú.
        self.menu_dialogues = [
            "Atacar o curarse?",
            "Eliminar el virus te llena de determinacion",
            "El virus te está observando",
            "Un golpe menos",
            "El Virus busca venganza",
            "Tu computadora no sanara sola",
            "Tratas de comprender la figura del enemigo",
            "El enemigo te clava la mirada",
            "Preferirias estar en la cama",
            "No aprobaras el examen si no lo eliminas",
            "Te sientes debil",
            "El virus hace poses extrañas",
            "El virus baila samba",
            "El virus esta burlando de tu nota de programacion",
            "Se nota que no es tu primer intento",
            "TLauncher te esta observando",
            "Saludos a la UTN",
            "Pulsa la X si queres",
            "Spyware detected",
            "El virus se aburre y mira TikTok",
            "Cick, Click",
            "Vos podes",
            "...",
            "....",
            ".....",
            "¿Dificil?",
            "El enemigo se ve pensativo",
            "El enemigo golpea al piso",
            "¿Virtual o real?",
            "¡Cuidado con el borde!",
            "El enemigo te muestra sus músculos",
            "Te falta odio",
            "El enemigo se ríe de ti",
            "Windows defender was disabled",
            "Pensaste que era un problema de volumen, pero era yo, el virus!",
            "El virus entro a %APPDATA%",
            "El virus se burla de tu falta de atención",
            "El virus: ez",
            "El virus: so easy",
            "El virus: gg no player",
            "El virus: Casi uso las manos",
            "El virus: Saludos a mi novia",
            "El virus: ¿como se le sube la dificultad al bot?",
            "La oscuridad revela la luz",
            "El dolor forja la fuerza",
            "La derrota es solo un paso hacia la victoria",
            "Tu vida: 3hp",
            "Tu determinacion: 15%",
            "Intentos: 67",
            "desinstalando Linkedin...",
            "Un gmail ha llegado: 'Felicidades has ganado un premio!!'",
            "Notificacion recibida: 'Если вы это читаете, вы молодец.' ",
            "El ejercito ruso manda",
            "No podes evitar lo inevitable",
            "La guerra nunca cambia",
            "Un simple programador no podra contra nuestro sistema",
            "La tecnologia Rusa es la mas poderosa del mundo",
            "JJBA es el mejor anime",
            "y sí si?",
            "¿Por qué no?",
            "Si fuera dev, definitivamente no usaria Pygame",
            "Linux es superior",
            "La abundancia es lo mismo que la insuficiencia",
            "Sabes mucho",
            "nicki nicole si o no",
            "¿Esto me convierte en un hacker?",
            

            # Los textos en ruso estan hechos a proposito y es parte de la historia del juego
            "Война не закончится, пока мы этого не скажем.",
            "Программисты не смогут предотвратить наше вторжение.",
            "суперядро будет нашим",
            "Мы уже все знаем о твоей бабушке, отпусти нас, и мы не причиним ей вреда.",
            "Если вы нас устраните, вы будете следующим, кого мы будем искать."

        ]
        self._menu_dialog_current = None
        self._menu_dialog_color = (240, 240, 255)
        self._menu_dialog_margin = 14

        # Seleccionar diálogo para el primer menú
        self._pick_menu_dialog()

        # --- AI Chat System ---
        self.chat_active = False
        self.chat_input = ""
        self.chat_response = ""
        self.chat_loading = False
        self.chat_error = ""
        self._c_prev = False
        self._enter_prev = False
        self._backspace_prev = False
        self.chat_font = pygame.font.Font(None, 28)
        self.chat_prompt_color = (100, 255, 100)  # Verde para tu texto
        self.chat_response_color = (255, 100, 100)  # Rojo para respuesta del virus
        
        # Verificar si OpenAI está disponible
        self.openai_available = False
        if hasattr(c, 'OPENAI_API_KEY') and c.OPENAI_API_KEY:
            try:
                import openai
                self.openai = openai
                self.openai.api_key = c.OPENAI_API_KEY
                self.openai_available = True
                print("✅ OpenAI configurado correctamente")
            except ImportError:
                print("⚠️ OpenAI no instalado. Ejecuta: pip install openai")
            except Exception as e:
                print(f"⚠️ Error configurando OpenAI: {e}")
        else:
            print("⚠️ OPENAI_API_KEY no configurada en Const.py")

        # Fallback offline (respuestas simuladas) para errores (cuota / red)
        self.ai_fallback_enabled = getattr(c, 'AI_FALLBACK_ON_ERROR', True)
        self.fallback_responses = [
            "Sistema comprometido...",
            "Tu defensa es patética",
            "La red me pertenece",
            "Rusia observa, jugador",
            "Código frágil, mente débil",
            "No podrás detenerme",
            "Procesando tu derrota",
            "Kernel infectado ya",
            "Tus intentos: inútiles",
            "Mi expansión continúa"
        ]

    def _pick_menu_dialog(self):
        if not self.menu_dialogues:
            self._menu_dialog_current = None
            return
        self._menu_dialog_current = random.choice(self.menu_dialogues)

    def _call_openai_api(self, user_message):
        """Llama a la API de OpenAI en un thread separado"""
        try:
            # Usar el nuevo formato de OpenAI (v1.0+)
            from openai import OpenAI
            client = OpenAI(api_key=c.OPENAI_API_KEY)
            
            system_prompt = getattr(c, 'OPENAI_PROMPT', 
                "Eres un virus maligno. Responde de forma corta y amenazante.")
            
            # Usar configuración del modelo y tokens desde Const.py
            model = getattr(c, 'OPENAI_MODEL', 'gpt-3.5-turbo')
            max_tokens = getattr(c, 'OPENAI_MAX_TOKENS', 30)
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=0.9
            )
            
            self.chat_response = response.choices[0].message.content.strip()
            self.chat_loading = False
            print(f"🤖 Respuesta IA ({model}, {max_tokens} tokens): {self.chat_response}")
            
        except Exception as e:
            err_text = str(e)
            print(f"❌ Error OpenAI: {err_text}")
            quota = ('insufficient_quota' in err_text.lower() or '429' in err_text)
            if quota and self.ai_fallback_enabled:
                # Usar respuesta simulada
                self.chat_response = random.choice(self.fallback_responses)
                self.chat_error = "(sin cuota - usando simulación)"
                self.chat_loading = False
                print("🔁 Usando fallback offline por cuota excedida")
            else:
                self.chat_error = f"Error: {err_text[:70]}"
                self.chat_loading = False

    def start_chat(self):
        """Activa el modo de chat con la IA"""
        self.chat_active = True
        self.chat_input = ""
        self.chat_response = ""
        self.chat_loading = False
        
        if not self.openai_available:
            self.chat_error = "OpenAI no esta configurado. Revisa Const.py y lee RESUMEN_CHAT.md"
            print("⚠️ Chat abierto pero OpenAI no disponible")
        else:
            self.chat_error = ""
            print("💬 Chat activado - Escribe tu mensaje y presiona ENTER")

    def send_chat_message(self):
        """Envía el mensaje del usuario a OpenAI"""
        if not self.chat_input.strip():
            return
        
        if not self.openai_available:
            if self.ai_fallback_enabled:
                self.chat_response = random.choice(self.fallback_responses)
                self.chat_error = "(sin API - respuesta simulada)"
                self.chat_loading = False
                print("🔁 Fallback sin API key - simulando respuesta")
                self.chat_input = ""
                return
            else:
                self.chat_error = "OpenAI no esta configurado. Instala con: pip install openai"
                print("⚠️ Intento de enviar mensaje sin OpenAI configurado")
                return
        
        self.chat_loading = True
        self.chat_error = ""
        user_msg = self.chat_input
        self.chat_input = ""
        self.chat_input = ""
        
        # Llamar API en thread para no bloquear el juego
        thread = threading.Thread(target=self._call_openai_api, args=(user_msg,))
        thread.daemon = True
        thread.start()
        print(f"📤 Enviando a IA: {user_msg}")

    def close_chat(self):
        """Cierra el chat y vuelve al menú"""
        self.chat_active = False
        self.chat_input = ""
        self.chat_response = ""
        self.chat_error = ""
        print("❌ Chat cerrado")

    

    def _wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if font.size(test)[0] <= max_width:
                line = test
            else:
                if line:
                    lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def enter_menu(self):
        self.state = "menu"
        self._pick_menu_dialog()

    def _pressed_once(self, now, prev_attr):
        prev = getattr(self, prev_attr)
        setattr(self, prev_attr, now)
        return now and not prev

    def update(self, player, enemy):
        keys = pygame.key.get_pressed()

        # Si el chat está activo, manejar input de texto
        if self.chat_active:
            return  # No procesar combate mientras se chatea

        left_once = self._pressed_once(keys[pygame.K_LEFT], "_left_prev")
        right_once = self._pressed_once(keys[pygame.K_RIGHT], "_right_prev")
        x_once = self._pressed_once(keys[pygame.K_x], "_x_prev")
        c_once = self._pressed_once(keys[pygame.K_c], "_c_prev")

        if self.state == "menu":
            # Presionar C para abrir chat con la IA
            if c_once:
                self.start_chat()
                return

            if left_once:
                self.selected = 0
            if right_once:
                self.selected = 1

            if x_once:
                if self.selected == 0:
                    if self.attack_sound:
                        print("▶️ Reproduciendo Attack.wav")
                        self.attack_sound.play()
                    if enemy:
                        self.attack_effect = AttackEffect(enemy.rect)
                        self.enemy_shake_timer = 10
                        self.enemy_base_pos = enemy.rect.topleft
                        # Use enemy.hit so phase transitions and side-effects run
                        try:
                            enemy.hit()
                        except Exception:
                            # Fallback to direct HP decrement if method missing
                            enemy.hp -= 10
                    self.state = "ataque"
                else:
                    player.hp = min(player.hp + 15, 20)
                    if self.curarse_sound:
                        print("▶️ Reproduciendo healup.mp3")
                        self.curarse_sound.play()
                    else:
                        print("❌ No se pudo reproducir healup.mp3")
                    self.state = "defensa"
                    self.timer = 0

        elif self.state == "ataque":
            if hasattr(enemy, 'silencio_activo') and enemy.silencio_activo:
                return
            if self.attack_effect:
                self.attack_effect.update()
                if self.attack_effect.finished:
                    self.attack_effect = None
                    self.state = "defensa"
                    self.timer = 0
            else:
                self.state = "defensa"
                self.timer = 0

        elif self.state == "defensa":
            self.timer += 1
            if self.timer >= self.DEFENSA_DUR:
                self.enter_menu()

        if self.enemy_shake_timer > 0 and enemy:
            offset = (-2, 2)[self.enemy_shake_timer % 2]
            enemy.rect.topleft = (self.enemy_base_pos[0] + offset, self.enemy_base_pos[1])
            self.enemy_shake_timer -= 1
            if self.enemy_shake_timer == 0:
                enemy.rect.topleft = self.enemy_base_pos

    def handle_chat_event(self, event):
        """Maneja eventos de teclado para el chat"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # ESC para cerrar chat
                self.close_chat()
            elif event.key == pygame.K_RETURN:
                # ENTER para enviar mensaje
                if not self.chat_loading:
                    self.send_chat_message()
            elif event.key == pygame.K_BACKSPACE:
                # Borrar último carácter
                self.chat_input = self.chat_input[:-1]
            else:
                # Agregar caracteres (letras, números, espacios, etc.)
                if len(self.chat_input) < 100:  # Límite de 100 caracteres
                    if event.unicode and event.unicode.isprintable():
                        self.chat_input += event.unicode

    def draw(self, screen, enemy=None):
        # Si el chat está activo, mostrar interfaz de chat
        if self.chat_active:
            self._draw_chat(screen)
            return

        if self.state == "menu":
            opciones = ["ATACAR", "CURARSE"]
            
            # Determinar qué sprites usar
            sprites = [
                (self.atacar_selected if self.selected == 0 else self.atacar_normal),
                (self.curarse_selected if self.selected == 1 else self.curarse_normal)
            ]
            
            for i, (texto, sprite) in enumerate(zip(opciones, sprites)):
                x = c.ANCHO // 2 + (i * 200) - 100
                y = c.ALTO - 80
                
                # Si el sprite existe, dibujarlo; si no, usar texto
                if sprite:
                    sprite_rect = sprite.get_rect(center=(x, y))
                    screen.blit(sprite, sprite_rect)
                else:
                    # Fallback a texto
                    color = c.AMARILLO if i == self.selected else c.BLANCO
                    render = self.font.render(texto, True, color)
                    rect = render.get_rect(center=(x, y))
                    screen.blit(render, rect)

            # Dibujar diálogo de menú dentro del border
            if self._menu_dialog_current:
                max_w = c.BOX_ANCHO - self._menu_dialog_margin * 2
                lines = self._wrap_text(self._menu_dialog_current, self.font, max_w)
                # Caja de fondo sutil
                box_h = 8 + len(lines) * (self.font.get_height() + 2)
                box_rect = pygame.Rect(c.BOX_X + self._menu_dialog_margin,
                                       c.BOX_Y + self._menu_dialog_margin,
                                       max_w,
                                       box_h)
                bg = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
                bg.fill((10, 10, 30, 120))
                screen.blit(bg, box_rect.topleft)
                # Texto
                y = box_rect.top + 4
                for ln in lines:
                    surf = self.font.render(ln, True, self._menu_dialog_color)
                    screen.blit(surf, (box_rect.left + 4, y))
                    y += self.font.get_height() + 2

            # Mostrar hint para abrir chat
            hint_text = "Presiona C para hablar con el virus"
            hint_surf = self.chat_font.render(hint_text, True, (180, 180, 200))
            hint_rect = hint_surf.get_rect(center=(c.ANCHO // 2, c.ALTO - 120))
            screen.blit(hint_surf, hint_rect)

        elif self.state == "ataque":
            if enemy and hasattr(enemy, 'silencio_activo') and enemy.silencio_activo:
                return
            msg = self.font.render("¡ATACASTE!", True, c.ROJO)
            screen.blit(msg, (c.ANCHO // 2 - 80, c.ALTO - 100))

        if self.attack_effect:
            screen.blit(self.attack_effect.image, self.attack_effect.rect)

    def _draw_chat(self, screen):
        """Dibuja la interfaz de chat dentro del border"""
        max_w = c.BOX_ANCHO - 20
        x_start = c.BOX_X + 10
        y_start = c.BOX_Y + 10
        
        # Fondo oscuro para el chat
        chat_bg = pygame.Surface((c.BOX_ANCHO, c.BOX_ALTO), pygame.SRCALPHA)
        chat_bg.fill((5, 5, 15, 220))
        screen.blit(chat_bg, (c.BOX_X, c.BOX_Y))
        
        y_offset = y_start
        
        # Título
        title = self.font.render("CHAT CON EL VIRUS", True, (255, 255, 255))
        screen.blit(title, (x_start, y_offset))
        y_offset += 45
        
        # Mostrar input del usuario
        input_label = self.chat_font.render("Tu mensaje:", True, self.chat_prompt_color)
        screen.blit(input_label, (x_start, y_offset))
        y_offset += 30
        
        # Caja de input con cursor parpadeante
        input_text = self.chat_input
        if pygame.time.get_ticks() % 1000 < 500:  # Cursor parpadeante
            input_text += "|"
        
        input_lines = self._wrap_text(input_text, self.chat_font, max_w - 20)
        for line in input_lines:
            surf = self.chat_font.render(line, True, (255, 255, 255))
            screen.blit(surf, (x_start + 10, y_offset))
            y_offset += 28
        
        y_offset += 10
        
        # Mostrar estado/respuesta
        if self.chat_loading:
            loading_text = "Esperando respuesta..."
            loading_surf = self.chat_font.render(loading_text, True, (255, 255, 100))
            screen.blit(loading_surf, (x_start, y_offset))
        elif self.chat_error and not self.chat_response:
            # Sólo error (sin fallback)
            error_lines = self._wrap_text(self.chat_error, self.chat_font, max_w - 20)
            for line in error_lines:
                surf = self.chat_font.render(line, True, (255, 100, 100))
                screen.blit(surf, (x_start, y_offset))
                y_offset += 28
        elif self.chat_response:
            response_label = self.chat_font.render("Virus dice:", True, self.chat_response_color)
            screen.blit(response_label, (x_start, y_offset))
            y_offset += 30
            
            response_lines = self._wrap_text(self.chat_response, self.chat_font, max_w - 20)
            for line in response_lines:
                surf = self.chat_font.render(line, True, (255, 200, 200))
                screen.blit(surf, (x_start + 10, y_offset))
                y_offset += 28
            if self.chat_error:
                # Mostrar nota de fallback debajo si existe
                note_lines = self._wrap_text(self.chat_error, self.chat_font, max_w - 20)
                for line in note_lines:
                    surf = self.chat_font.render(line, True, (200, 140, 80))
                    screen.blit(surf, (x_start + 10, y_offset))
                    y_offset += 24
        
        # Instrucciones en la parte inferior
        y_bottom = c.BOX_Y + c.BOX_ALTO - 50
        inst1 = self.chat_font.render("ENTER = Enviar | ESC = Salir", True, (150, 150, 150))
        screen.blit(inst1, (x_start, y_bottom))

    def draw_defense_timer_bar(self, screen: pygame.Surface):
        """Dibuja una barra delgada arriba del border que se achica con el tiempo de defensa restante."""
        # Calcular progreso restante (1.0 -> 0.0)
        dur = max(1, getattr(self, 'DEFENSA_DUR', 1))
        t = max(0, min(self.timer, dur))
        frac_left = 1.0 - (t / dur)

        # Geometría de la barra
        full_w = c.BOX_ANCHO
        bar_w = int(full_w * frac_left)
        bar_h = self.defense_bar_height
        x = c.BOX_X
        y = max(0, c.BOX_Y - self.defense_bar_margin - bar_h)

        # Fondo (track) semi-transparente del ancho completo
        track = pygame.Surface((full_w, bar_h), pygame.SRCALPHA)
        track.fill(self.defense_bar_bg)
        screen.blit(track, (x, y))

        # Barra restante (se achica con el tiempo)
        if bar_w > 0:
            rect_fg = pygame.Rect(x, y, bar_w, bar_h)
            pygame.draw.rect(screen, self.defense_bar_fg, rect_fg)
