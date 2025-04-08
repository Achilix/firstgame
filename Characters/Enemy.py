import pygame
pygame.mixer.init()
zombie_sound = pygame.mixer.Sound("assets/zombie.mp3")

class Enemy:
    def __init__(self, x, y, width, height, enemy_sprite):
        self.sprite_sheet_walk = pygame.image.load('SPRITES/Enemy/Walk.png').convert_alpha()
        self.frames_walk = self.load_frames(self.sprite_sheet_walk, num_frames=10)
        self.sprite_sheet_dead = pygame.image.load('SPRITES/Enemy/Dead.png').convert_alpha()
        self.frames_dead = self.load_frames(self.sprite_sheet_dead, num_frames=5)
        self.current_frame = 0
        self.animation_speed = 0.1
        self.image = self.frames_walk[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect.y = y - (self.rect.height - height)
        self.speed = 1
        self.flipped = False
        self.health = 100
        self.is_dead = False
        self.death_animation_done = False
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity_y = 0
        self.gravity = 0.5
        self.sound_timer = 0

    def load_frames(self, sprite_sheet, num_frames):
        frames = []
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width,
                0,
                frame_width,
                frame_height
            ))
            frame = pygame.transform.scale(frame, (int(frame_width * 1.5), int(frame_height * 1.5)))
            frames.append(frame)
        return frames

    def animate(self):
        if self.is_dead:
            if not self.death_animation_done:
                self.current_frame += self.animation_speed
                if self.current_frame >= len(self.frames_dead):
                    self.current_frame = len(self.frames_dead) - 1
                    self.death_animation_done = True
                self.image = self.frames_dead[int(self.current_frame)]
        else:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_walk):
                self.current_frame = 0
            self.image = self.frames_walk[int(self.current_frame)]
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)

    def play_sound(self):
        if self.sound_timer <= 0:
            zombie_sound.play()
            self.sound_timer = 300

    def update(self, camera):
        if camera.apply(self.rect).colliderect(pygame.Rect(0, 0, camera.width, camera.height)):
            self.play_sound()
        if self.sound_timer > 0:
            self.sound_timer -= 1
        self.animate()

    def apply_gravity(self, blocks):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = block.rect.top
                    self.velocity_y = 0

    def move_toward_player(self, player, blocks):
        if not self.is_dead:
            self.apply_gravity(blocks)
            player_in_sight = abs(self.rect.x - player.rect.x) < 300 and abs(self.rect.y - player.rect.y) < 50
            if player_in_sight:
                if self.rect.x < player.rect.x:
                    self.flipped = False
                    self.rect.x += self.speed
                elif self.rect.x > player.rect.x:
                    self.flipped = True
                    self.rect.x -= self.speed
            else:
                if not hasattr(self, "patrol_direction"):
                    self.patrol_direction = 5
                    self.patrol_start_x = self.rect.x
                    self.patrol_range = 100
                self.rect.x += self.speed * self.patrol_direction
                if self.rect.x > self.patrol_start_x + self.patrol_range:
                    self.patrol_direction = -1
                    self.flipped = True
                elif self.rect.x < self.patrol_start_x:
                    self.patrol_direction = 1
                    self.flipped = False
            for block in blocks:
                if self.rect.colliderect(block.rect):
                    if self.rect.x < block.rect.x:
                        self.rect.right = block.rect.left
                        self.patrol_direction = -1
                    elif self.rect.x > block.rect.x:
                        self.rect.left = block.rect.right
                        self.patrol_direction = 1

    def take_damage(self, amount):
        if self.is_dead:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            zombie_sound.play()

    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))
        if not self.is_dead:
            health_bar_bg_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
            pygame.draw.rect(screen, (255, 0, 0), camera.apply(health_bar_bg_rect))
            health_bar_fg_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5)
            pygame.draw.rect(screen, (0, 255, 0), camera.apply(health_bar_fg_rect))