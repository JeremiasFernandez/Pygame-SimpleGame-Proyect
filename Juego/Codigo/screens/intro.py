import pygame, os
import Const as c

class IntroTopdown:
    def __init__(self):
        # Load player directional sprites (fallback to colored squares)
        base = os.path.join("Juego", "assets", "Sprites", "mas_sprites")
        self.sprites = {}
        self.sprites['down'] = self._load_or_fallback(os.path.join(base, "prota_down.png"), (84, 108), (80,160,255))
        self.sprites['up']   = self._load_or_fallback(os.path.join(base, "prota_up.png"),   (84, 108), (80,255,160))
        self.sprites['left'] = self._load_or_fallback(os.path.join(base, "prota_left.png"), (84, 108), (255,200,80))
        self.sprites['right']= self._load_or_fallback(os.path.join(base, "prota_right.png"),(84, 108), (255,120,120))
        # Optional walking animation sheets 1x4 per direction
        self.anim_frames = {
            'down': self._load_anim_row(os.path.join(base, "prota_walk_down.png"), (112,144)),
            'up':   self._load_anim_row(os.path.join(base, "prota_walk_up.png"),   (112,144)),
            'left': self._load_anim_row(os.path.join(base, "prota_walk_left.png"), (112,144)),
            'right':self._load_anim_row(os.path.join(base, "prota_walk_right.png"),(112,144)),
        }
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_delay = 7  # frames per animation step
        self.is_moving = False
        self.face_prota = self._load_or_fallback(os.path.join(base, "player_cara.png"), (96,96), (120,180,255))
        self.face_grand = self._load_or_fallback(os.path.join(base, "abuela_face.png"), (96,96), (255,200,160))

        # Room background image (800x600)
        try:
            self.room_bg = pygame.image.load(os.path.join(base, "room.png")).convert()
            # Ensure it's exactly screen size
            if self.room_bg.get_size() != (c.ANCHO, c.ALTO):
                self.room_bg = pygame.transform.scale(self.room_bg, (c.ANCHO, c.ALTO))
        except Exception:
            self.room_bg = None  # fallback to drawn room

        # PC GIF animation
        self.pc_frames = []
        self.pc_frame_index = 0
        self.pc_frame_timer = 0
        self.pc_frame_delay = 8
        self._load_pc_gif(os.path.join(base, "pc.gif"))

        # Grandma sprite
        self.grandma_sprite = self._load_or_fallback(os.path.join(base, "grandma.png"), (80, 104), (180,130,90))

        # Sounds
        try:
            self.select_snd = pygame.mixer.Sound(os.path.join("Juego","assets","Sounds","menu_select.wav"))
        except Exception:
            self.select_snd = None
        
        try:
            self.jump_snd = pygame.mixer.Sound(os.path.join("Juego","assets","Sounds","jump.wav"))
        except Exception:
            # Fallback to menu_select if jump.wav doesn't exist
            self.jump_snd = self.select_snd

        # World layout (simple room)
        self.room_rect = pygame.Rect(120, 80, c.ANCHO-240, c.ALTO-200)  # inner walk area
        # Objects (visual position)
        self.pc_rect = pygame.Rect(self.room_rect.right-120, self.room_rect.top+40, 60, 40)
        self.grandma_rect = pygame.Rect(self.room_rect.left+60, self.room_rect.top+60, 40, 52)
        
        # Collision boxes (smaller, at the top border - wall collision)
        self.pc_collision = pygame.Rect(self.pc_rect.x, self.pc_rect.y, self.pc_rect.width, 15)
        self.grandma_collision = pygame.Rect(self.grandma_rect.x, self.grandma_rect.y, self.grandma_rect.width, 15)

        # Player
        self.pos = pygame.Vector2(self.room_rect.centerx, self.room_rect.bottom-80)
        self.speed = 2.6
        self.facing = 'down'
        self.player_rect = pygame.Rect(0,0, 22, 30)
        self._update_player_rect()

        # Dialog state
        self.dialog_active = True
        self.dialog_queue = [
            { 'text': "Mi amor… tengo un problema con el volumen de mi computadora.", 'face': self.face_grand },
            { 'text': "El típico problema de los ancianos…", 'face': self.face_prota },
        ]
        self.current_dialog = self.dialog_queue.pop(0) if self.dialog_queue else None
        self.font = pygame.font.Font(None, 28)

        # UI hints
        self.show_pc_hint = False
        self.show_grand_hint = False

        # Jump animation (small hop when pressing X)
        self.jump_active = False
        self.jump_timer = 0
        self.jump_duration = 15  # frames
        self.jump_offset = 0  # vertical offset for jump

        # Battle transition animation (Undertale-style screen flash)
        self.battle_transition_active = False
        self.battle_transition_timer = 0
        self.battle_transition_duration = 60  # ~1 second at 60 FPS
        self.flash_pattern = [  # Pattern of flashes (frames to show black screen)
            (0, 8),    # Flash 1: frames 0-8
            (12, 20),  # Flash 2: frames 12-20
            (24, 32),  # Flash 3: frames 24-32
            (40, 60),  # Final fade to black: frames 40-60
        ]
        
        # Battle transition sound
        try:
            self.battle_transition_snd = pygame.mixer.Sound(os.path.join("Juego","assets","Sounds","battle.wav"))
            self.battle_transition_snd.set_volume(0.5)
        except Exception:
            # Try alternative names
            try:
                self.battle_transition_snd = pygame.mixer.Sound(os.path.join("Juego","assets","Sounds","encounter.wav"))
                self.battle_transition_snd.set_volume(0.5)
            except Exception:
                self.battle_transition_snd = self.select_snd  # Use menu select as fallback
                print("[WARNING] No se pudo cargar sonido de transición de batalla, usando fallback")

    def _load_or_fallback(self, path, size, color):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except Exception:
            surf = pygame.Surface(size, pygame.SRCALPHA)
            surf.fill((*color, 255))
            return surf

    def _update_player_rect(self):
        self.player_rect.center = (int(self.pos.x), int(self.pos.y))

    def _load_pc_gif(self, path):
        """Load PC GIF and extract frames."""
        try:
            from PIL import Image
            gif = Image.open(path)
            frames = []
            try:
                while True:
                    frame = gif.convert("RGBA")
                    # Scale to fit PC area
                    frame = frame.resize((100, 80), Image.Resampling.LANCZOS)
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    py_img = pygame.image.fromstring(data, size, mode)
                    frames.append(py_img)
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass
            self.pc_frames = frames if frames else []
        except Exception as e:
            # Fallback: create simple animated rectangle
            self.pc_frames = []

    def _load_anim_row(self, path, scale_to, frames=4):
        """Load a 1x4 spritesheet row and slice into frames; return list of Surfaces or None."""
        try:
            sheet = pygame.image.load(path).convert_alpha()
            fw = sheet.get_width() // frames
            fh = sheet.get_height()
            out = []
            for i in range(frames):
                frame = sheet.subsurface(pygame.Rect(i*fw, 0, fw, fh)).copy()
                if scale_to:
                    frame = pygame.transform.scale(frame, scale_to)
                out.append(frame)
            return out
        except Exception:
            return None

    def handle_event(self, event):
        # Advance dialogs with X
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            # Trigger jump animation and sound
            if not self.dialog_active:
                self.jump_active = True
                self.jump_timer = 0
                if self.jump_snd:
                    self.jump_snd.set_volume(0.05)
                    self.jump_snd.play()
            
            if self.dialog_active:
                if self.dialog_queue:
                    self.current_dialog = self.dialog_queue.pop(0)
                else:
                    self.dialog_active = False
                    self.current_dialog = None
                    # after intro dialog, allow movement/interaction
                return None
            # Interactions when no dialog
            # Near PC -> start battle transition
            if self._near(self.player_rect, self.pc_rect, 28):
                if not self.battle_transition_active:
                    self.battle_transition_active = True
                    self.battle_transition_timer = 0
                    if self.battle_transition_snd:
                        self.battle_transition_snd.play()
                return None  # Don't return 'start_battle' yet
            # Near Grandma -> start grandma dialog variations
            if self._near(self.player_rect, self.grandma_rect, 28):
                self.dialog_active = True
                self.dialog_queue = [
                    { 'text': "¿Podés ayudarme con la PC? No entiendo nada.", 'face': self.face_grand },
                    { 'text': "Ya voy, abue. Primero acercarme al CPU y presionar X.", 'face': self.face_prota },
                ]
                self.current_dialog = self.dialog_queue.pop(0)
                return None
        return None

    def _near(self, a: pygame.Rect, b: pygame.Rect, dist: int):
        ax, ay = a.center
        bx, by = b.center
        return (abs(ax-bx) <= dist) and (abs(ay-by) <= dist)

    def update(self):
        # Battle transition has priority over everything
        if self.battle_transition_active:
            self.battle_transition_timer += 1
            if self.battle_transition_timer >= self.battle_transition_duration:
                # Transition complete, signal to start battle
                return 'start_battle'
            return None  # Continue showing transition
        
        # Movement disabled when dialog active
        keys = pygame.key.get_pressed()
        if not self.dialog_active:
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= 1; self.facing = 'left'
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += 1; self.facing = 'right'
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy -= 1; self.facing = 'up'
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += 1; self.facing = 'down'
            # normalize
            if dx or dy:
                v = pygame.Vector2(dx, dy)
                if v.length() != 0:
                    v = v.normalize() * self.speed
                    # Save old position
                    old_x, old_y = self.pos.x, self.pos.y
                    # Try to move
                    self.pos.x += v.x
                    self.pos.y += v.y
                    # clamp to room
                    self.pos.x = max(self.room_rect.left+10, min(self.room_rect.right-10, self.pos.x))
                    self.pos.y = max(self.room_rect.top+10, min(self.room_rect.bottom-10, self.pos.y))
                    # Update player rect to check collisions
                    self._update_player_rect()
                    # Check collision with PC and Grandma (using smaller collision boxes)
                    if self.player_rect.colliderect(self.pc_collision) or self.player_rect.colliderect(self.grandma_collision):
                        # Revert to old position
                        self.pos.x, self.pos.y = old_x, old_y
                        self._update_player_rect()
            # walk animation state
            self.is_moving = bool(dx or dy)
            if self.is_moving and self.anim_frames.get(self.facing):
                self.anim_timer += 1
                if self.anim_timer >= self.anim_delay:
                    self.anim_timer = 0
                    self.anim_index = (self.anim_index + 1) % len(self.anim_frames[self.facing])
            else:
                self.anim_index = 0
                self.anim_timer = 0
            self._update_player_rect()

        # Animate PC GIF
        if self.pc_frames:
            self.pc_frame_timer += 1
            if self.pc_frame_timer >= self.pc_frame_delay:
                self.pc_frame_timer = 0
                self.pc_frame_index = (self.pc_frame_index + 1) % len(self.pc_frames)

        # Update jump animation
        if self.jump_active:
            self.jump_timer += 1
            # Small parabola for jump (0 to jump_duration)
            progress = self.jump_timer / self.jump_duration
            if progress <= 0.5:
                # Going up
                self.jump_offset = -20 * (progress * 2)  # max -14 pixels at halfway
            else:
                # Coming down
                self.jump_offset = -20 * (2 - progress * 2)
            
            if self.jump_timer >= self.jump_duration:
                self.jump_active = False
                self.jump_timer = 0
                self.jump_offset = 0

        # hints
        self.show_pc_hint = (not self.dialog_active) and self._near(self.player_rect, self.pc_rect, 30)
        self.show_grand_hint = (not self.dialog_active) and self._near(self.player_rect, self.grandma_rect, 26)

    def draw(self, screen):
        # Room background: use image if available, else draw simple room
        if self.room_bg:
            screen.blit(self.room_bg, (0, 0))
        else:
            # Simple room background (fallback)
            screen.fill((24, 20, 28))
            # floor
            floor = pygame.Rect(self.room_rect)
            pygame.draw.rect(screen, (46,42,60), floor)
            # walls
            pygame.draw.rect(screen, (80, 70, 100), floor, 6)

        # Draw PC GIF (on top of background)
        if self.pc_frames:
            frame = self.pc_frames[self.pc_frame_index]
            rect = frame.get_rect(center=self.pc_rect.center)
            screen.blit(frame, rect)
        else:
            # Fallback: draw simple PC
            pygame.draw.rect(screen, (60,60,60), self.pc_rect)
            mon = self.pc_rect.copy(); mon.width = self.pc_rect.width-16; mon.height = self.pc_rect.height-12; mon.move_ip(8,2)
            pygame.draw.rect(screen, (120,180,255), mon)

        # Draw Grandma (on top of background)
        grand_rect = self.grandma_sprite.get_rect(midbottom=self.grandma_rect.midbottom)
        screen.blit(self.grandma_sprite, grand_rect)

        # Draw player (animated if sheet exists)
        frames = self.anim_frames.get(self.facing)
        if frames:
            frame = frames[self.anim_index if self.is_moving else 0]
            rect = frame.get_rect(center=self.player_rect.center)
            # Apply jump offset
            rect.y += int(self.jump_offset)
            screen.blit(frame, rect)
        else:
            sprite = self.sprites.get(self.facing, self.sprites['down'])
            rect = sprite.get_rect(center=self.player_rect.center)
            # Apply jump offset
            rect.y += int(self.jump_offset)
            screen.blit(sprite, rect)

        # Hints
        if self.show_pc_hint:
            self._draw_hint(screen, "Presiona X para revisar", (self.pc_rect.centerx, self.pc_rect.top-18))
        if self.show_grand_hint:
            self._draw_hint(screen, "Presiona X para hablar", (self.grandma_rect.centerx, self.grandma_rect.top-18))

        # Dialog Box
        if self.dialog_active and self.current_dialog:
            self._draw_dialog_box(screen, self.current_dialog['text'], self.current_dialog.get('face'))
        
        if self.battle_transition_active:
            self._draw_battle_transition(screen)

    def _draw_battle_transition(self, screen):
        t = self.battle_transition_timer
        show_black = False
        alpha = 255
        
        
        for start, end in self.flash_pattern:
            if start <= t < end:
                show_black = True

                if start == 40:  
                    progress = (t - start) / (end - start)
                    alpha = int(255 * progress)
                break
        
        if show_black:
            overlay = pygame.Surface((c.ANCHO, c.ALTO))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))

    def _draw_hint(self, screen, text, pos):
        surf = self.font.render(text, True, c.BLANCO)
        bg = pygame.Surface((surf.get_width()+16, surf.get_height()+10), pygame.SRCALPHA)
        bg.fill((0,0,0,160))
        r = bg.get_rect(center=pos)
        screen.blit(bg, r)
        screen.blit(surf, surf.get_rect(center=pos))

    def _draw_dialog_box(self, screen, text, face_surface):
        box_h = 90
        box = pygame.Rect(20, c.ALTO - box_h - 20, c.ANCHO - 40, box_h)
        pygame.draw.rect(screen, (0,0,0,200), box)
        pygame.draw.rect(screen, (220,220,220), box, 2)


        if face_surface:
            face_rect = face_surface.get_rect()
            face_rect.midright = (box.right - 16, box.centery)
            screen.blit(face_surface, face_rect)
            text_area = pygame.Rect(box.left+16, box.top+12, box.width - face_rect.width - 48, box.height-24)
        else:
            text_area = pygame.Rect(box.left+16, box.top+12, box.width-32, box.height-24)


        self._render_text(screen, text, text_area, self.font, c.BLANCO)

    def _render_text(self, screen, text, rect, font, color):

        words = text.split(' ')
        line = ''
        y = rect.top
        space_w, _ = font.size(' ')
        while words:
            word = words.pop(0)
            test = (line + (' ' if line else '') + word)
            w, h = font.size(test)
            if w <= rect.width:
                line = test
            else:
                surf = font.render(line, True, color)
                screen.blit(surf, (rect.left, y))
                y += h + 6
                line = word
        if line:
            surf = font.render(line, True, color)
            screen.blit(surf, (rect.left, y))
