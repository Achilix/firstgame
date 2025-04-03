import pygame
import random
from Bullet import Bullet

class Player:
    def __init__(self, x, y, player_sprite, screen_width):
        # Load sprite sheets
        self.sprite_sheet_run = pygame.image.load('SPRITES/PLAYER/Run.png').convert_alpha()
        self.sprite_sheet_idle = pygame.image.load('SPRITES/PLAYER/Idle.png').convert_alpha()
        self.sprite_sheet_fire = pygame.image.load('SPRITES/PLAYER/Shot_1.png').convert_alpha()
        self.sprite_sheet_dead = pygame.image.load('SPRITES/PLAYER/Dead.png').convert_alpha()

        # Load animation frames
        self.frames_run = self.load_frames(self.sprite_sheet_run, num_frames=8)
        self.frames_idle = self.load_frames(self.sprite_sheet_idle, num_frames=7)
        self.frames_fire = self.load_frames(self.sprite_sheet_fire, num_frames=4)
        self.frames_dead = self.load_frames(self.sprite_sheet_dead, num_frames=4)

        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.frames_idle[self.current_frame]

        # Main rect for rendering and collision
        self.rect = self.image.get_rect(topleft=(x, y))

        # Create a mask for precise collision detection
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
        self.bullets = []
        self.bullet_count = 10

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
                self.current_frame += self.animation_speed
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

        # Update the mask whenever the image changes
        self.mask = pygame.mask.from_surface(self.image)

        return False

    def handle_input(self, keys, mouse_buttons):
        self.handle_movement(keys)

        if mouse_buttons[0]:
            self.shoot()

    def handle_movement(self, keys):
        self.is_moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            if not self.flipped:
                self.flipped = True
            self.is_moving = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width
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
            # Check for mask-based collision
            if platform.check_collision(self.mask, self.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.jumping = False

    def take_damage(self, amount, enemy_rect=None):
        """
        Reduce the player's health by the given amount.
        :param amount: The amount of damage to deal.
        :param enemy_rect: The rect of the enemy dealing the damage (optional).
        """
        if self.is_dead:
            return
        self.health -= amount
        print(f"Player took {amount} damage! Health: {self.health}")  # Debugging print
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            print("Player is dead!")  # Debugging print

    def shoot(self):
        if self.bullet_count > 0:
            if self.current_frame == 0:
                direction = -1 if self.flipped else 1
                bullet_x = self.rect.centerx + (direction * 20)
                bullet_y = self.rect.top + 91
                self.bullets.append(Bullet(bullet_x, bullet_y, direction))
                self.is_firing = True
                self.bullet_count -= 1
                print(f"Bullets left: {self.bullet_count}")
        else:
            print("Out of bullets!")

    def reload(self, amount):
        self.bullet_count += amount
        print(f"Reloaded! Bullets now: {self.bullet_count}")

    def update(self):
        if not self.is_dead:
            self.animate()
            self.update_bullets()
        else:
            if self.animate():
                print("Player death animation complete!")

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.right < 0 or bullet.rect.left > self.screen_width:
                self.bullets.remove(bullet)

    def draw(self, screen):
        # Draw the player
        screen.blit(self.image, self.rect.topleft)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw the health bar
        self.draw_health_bar(screen)

        # Draw the ammo count
        self.draw_ammo_count(screen)

    def draw_health_bar(self, screen):
        """
        Draw the player's health bar above their character.
        """
        bar_width = 100  # Width of the health bar
        bar_height = 10  # Height of the health bar
        bar_x = self.rect.centerx - bar_width // 2  # Center the bar above the player
        bar_y = self.rect.top - 20  # Position the bar slightly above the player

        # Calculate the health ratio
        health_ratio = self.health / 100

        # Draw the background of the health bar (gray)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Draw the foreground of the health bar (green)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def draw_ammo_count(self, screen):
        """
        Draw the player's ammo count on the screen.
        """
        font = pygame.font.Font(None, 36)  # Use a default font with size 36
        ammo_text = f"Ammo: {self.bullet_count}"
        text_surface = font.render(ammo_text, True, (255, 255, 255))  # White text
        screen.blit(text_surface, (10, 10))  # Display the ammo count at the top-left corner