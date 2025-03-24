import pygame
import random
from Bullet import Bullet
class Player:
    def __init__(self, x, y, player_sprite, screen_width):
        self.sprite_sheet_run = pygame.image.load('SPRITES/Run.png').convert_alpha()  # Running sprite sheet
        self.sprite_sheet_idle = pygame.image.load('SPRITES/Idle.png').convert_alpha()  # Idle sprite sheet
        self.sprite_sheet_fire = pygame.image.load('SPRITES/Shot_1.png').convert_alpha()  # Firing sprite sheet

        self.frames_run = self.load_frames(self.sprite_sheet_run, num_frames=8)  # 8 frames for running
        self.frames_idle = self.load_frames(self.sprite_sheet_idle, num_frames=7)  # 7 frames for idle
        self.frames_fire = self.load_frames(self.sprite_sheet_fire, num_frames=4)  # 4 frames for firing

        self.current_frame = 0
        self.animation_speed = 0.2  # Adjust animation speed
        self.image = self.frames_idle[self.current_frame]  # Start with idle animation
        self.rect = self.image.get_rect(topleft=(x, y))  # Use the default rect for the player

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.jump_height = 10
        self.flipped = False
        self.screen_width = screen_width  # Store screen width for boundary checks
        self.health = 100  # Player's health (out of 100)
        self.is_moving = False  # Track whether the player is moving
        self.is_firing = False  # Track whether the player is firing
        self.bullets = []  # List to store bullets

    def load_frames(self, sprite_sheet, num_frames):
        """
        Split the sprite sheet into individual frames.
        :param sprite_sheet: The loaded sprite sheet.
        :param num_frames: The total number of frames in the sprite sheet.
        :return: A list of frames.
        """
        frames = []
        frame_width = sprite_sheet.get_width() // num_frames  # Calculate the width of each frame
        frame_height = sprite_sheet.get_height()  # Use the full height of the sprite sheet

        for i in range(num_frames):
            # Extract each frame
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width,  # Start at the correct x-coordinate for each frame
                0,  # Start at the top of the sprite sheet
                frame_width,  # Width of the frame
                frame_height  # Height of the frame
            ))
            frames.append(frame)

        return frames

    def animate(self):
        """
        Handle the player's animation based on their state.
        """
        if self.is_firing:
            # Use shooting animation frames
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_fire):
                self.current_frame = 0
                self.is_firing = False  # Reset firing state after animation
            self.image = self.frames_fire[int(self.current_frame)]
        elif self.is_moving:
            # Use running animation frames
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_run):
                self.current_frame = 0
            self.image = self.frames_run[int(self.current_frame)]
        else:
            # Use idle animation frames
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_idle):
                self.current_frame = 0
            self.image = self.frames_idle[int(self.current_frame)]

        # Flip the image if the player is facing left
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def handle_input(self, keys, mouse_buttons):
        """
        Handle both keyboard and mouse input.
        :param keys: The pressed keys.
        :param mouse_buttons: The pressed mouse buttons.
        """
        self.handle_movement(keys)

        # Check for mouse button press (left mouse button)
        if mouse_buttons[0]:  # Left mouse button
            self.shoot()

    def handle_movement(self, keys):
        self.is_moving = False  # Assume the player is idle by default

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            if not self.flipped:
                self.flipped = True
            self.is_moving = True  # Player is moving

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width
            if self.flipped:
                self.flipped = False
            self.is_moving = True  # Player is moving

        if keys[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height

        # Animate based on movement state
        self.animate()

    def apply_gravity(self, platforms):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Collision with the platforms
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0 and self.rect.bottom >= platform.top:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.jumping = False

    def take_damage(self, amount, knockback_direction, zombie_rect):
        """
        Reduce the player's health and apply knockback.
        :param amount: The amount of damage to reduce from the player's health.
        :param knockback_direction: -1 for left, 1 for right.
        :param zombie_rect: The rectangle of the zombie causing the knockback.
        """
        if self.rect.colliderect(zombie_rect):  # Use the default rect for collision
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                print("Player is dead!")

    def shoot(self):
        """
        Shoot a bullet from the muzzle every first frame of the shooting animation.
        """
        if self.current_frame == 0:  # Fire only on the first frame of the shooting animation
            direction = -1 if self.flipped else 1  # -1 for left, 1 for right
            bullet_x = self.rect.centerx + (direction * 20)  # Offset bullet position horizontally
            bullet_y = self.rect.top + 91  # Muzzle position (91 pixels from the top)
            self.bullets.append(Bullet(bullet_x, bullet_y, direction))
            self.is_firing = True  # Trigger the firing animation

    def update(self):
        """
        Update the player's state (e.g., animation, bullets).
        """
        self.animate()
        self.update_bullets()

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.rect.right < 0 or bullet.rect.left > self.screen_width:
                self.bullets.remove(bullet)  # Remove bullets off-screen

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(screen)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        """
        Draw the player's health bar above their head.
        """
        bar_width = 50
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 10
        health_ratio = self.health / 100

        # Draw the background bar (gray)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Draw the health bar (green)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))