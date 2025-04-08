import pygame
from Bullet import Bullet
pygame.mixer.init()

class Player:
    def __init__(self, x, y, player_sprite, screen_width):
        Player.shooting_sound = pygame.mixer.Sound("assets/shooting.mp3")
        self.sprite_sheet_run = pygame.image.load('SPRITES/PLAYER/Run.png').convert_alpha()
        self.sprite_sheet_idle = pygame.image.load('SPRITES/PLAYER/Idle.png').convert_alpha()
        self.sprite_sheet_fire = pygame.image.load('SPRITES/PLAYER/Shot_1.png').convert_alpha()
        self.sprite_sheet_dead = pygame.image.load('SPRITES/PLAYER/Dead.png').convert_alpha()
        self.frames_run = self.load_frames(self.sprite_sheet_run, num_frames=8)
        self.frames_idle = self.load_frames(self.sprite_sheet_idle, num_frames=7)
        self.frames_fire = self.load_frames(self.sprite_sheet_fire, num_frames=4)
        self.frames_dead = self.load_frames(self.sprite_sheet_dead, num_frames=4)
        self.current_frame = 0
        self.animation_speed = 0.2
        self.death_animation_speed = 0.05
        self.death_animation_timer = 1
        self.image = self.frames_idle[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.jump_height = 10
        self.flipped = False
        self.screen_width = screen_width
        self.health = 100
        self.is_moving = False
        self.is_firing = False
        self.is_dead = False
        self.death_animation_done = False
        self.death_animation_frame = 0
        self.bullets = []
        self.bullet_cooldown = 0
        self.ammo_count = 20

    def load_frames(self, sprite_sheet, num_frames):
        frames = []
        frame_width = sprite_sheet.get_width() // num_frames
        frame_height = sprite_sheet.get_height()
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width, 0, frame_width, frame_height
            ))
            frames.append(frame)
        return frames

    def animate(self):
        if self.is_dead:
            if not self.death_animation_done:
                self.current_frame += self.death_animation_speed
                if self.current_frame >= len(self.frames_dead):
                    self.current_frame = len(self.frames_dead) - 1
                    self.death_animation_done = True
                self.image = self.frames_dead[int(self.current_frame)]
            else:
                return True
        elif self.is_firing:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_fire):
                self.current_frame = 0
                self.is_firing = False
            self.image = self.frames_fire[int(self.current_frame)]
        elif self.is_moving:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_run):
                self.current_frame = 0
            self.image = self.frames_run[int(self.current_frame)]
        else:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_idle):
                self.current_frame = 0
            self.image = self.frames_idle[int(self.current_frame)]
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)
        return False

    def play_death_animation(self):
        if not self.death_animation_done:
            self.death_animation_timer += self.death_animation_speed
            if self.death_animation_timer >= 1:
                self.death_animation_timer = 0
                self.death_animation_frame += 1
            if self.death_animation_frame < len(self.frames_dead):
                self.image = self.frames_dead[self.death_animation_frame]
            else:
                self.death_animation_done = True

    def handle_input(self, keys, mouse_buttons):
        self.handle_movement(keys)
        if mouse_buttons[0]:
            self.shoot()

    def handle_movement(self, keys):
        self.is_moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if not self.flipped:
                self.flipped = True
            self.is_moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.flipped:
                self.flipped = False
            self.is_moving = True
        if keys[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height
        self.animate()

    def apply_gravity(self, platforms):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        for platform in platforms:
            if platform.check_collision(self.mask, self.rect):
                if self.velocity_y > 0:
                    if self.rect.bottom - self.velocity_y <= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.jumping = False

    def take_damage(self, amount, enemy_rect=None):
        if self.is_dead:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dead = True

    def shoot(self):
        if self.bullet_cooldown == 0 and self.ammo_count > 0:
            direction = -1 if self.flipped else 1
            if self.flipped:
                bullet_x = self.rect.right - 83
            else:
                bullet_x = self.rect.left + 83
            bullet_y = self.rect.top + 90
            self.bullets.append(Bullet(bullet_x, bullet_y, direction))
            self.bullet_cooldown = 20
            self.ammo_count -= 1
            Player.shooting_sound.play()
            self.is_firing = True
            self.current_frame = 0

    def reload(self, amount):
        self.bullet_cooldown = max(self.bullet_cooldown - amount, 0)

    def update(self):
        if not self.is_dead:
            self.animate()
            self.update_bullets()
        else:
            if self.animate():
                pass

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_health_bar(self, screen, position=(10, 10)):
        bar_width = 100
        bar_height = 10
        bar_x, bar_y = position
        health_ratio = self.health / 100
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def draw_ammo_count(self, screen, position=(10, 30)):
        font = pygame.font.Font(None, 24)
        ammo_text = f"Ammo: {self.ammo_count}"
        text_surface = font.render(ammo_text, True, (255, 255, 255))
        screen.blit(text_surface, position)

    def draw_score(self, screen, score, position=(10, 50)):
        font = pygame.font.Font(None, 24)
        score_text = f"Score: {score}"
        text_surface = font.render(score_text, True, (255, 255, 255))
        screen.blit(text_surface, position)