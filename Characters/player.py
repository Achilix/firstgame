import pygame
import random
from Bullet import Bullet

# Initialize the mixer for sound effects
pygame.mixer.init()

class Player:
    # Class-level attributes for sound effects
    shooting_sound = None

    def __init__(self, x, y, player_sprite, screen_width):
        # Initialize sounds if not already initialized
        if Player.shooting_sound is None:
            Player.shooting_sound = pygame.mixer.Sound("assets/shooting.mp3")

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
        self.death_animation_speed = 0.05  # Slower speed for death animation
        self.death_animation_timer = 0  # Timer to control frame updates
        self.image = self.frames_idle[self.current_frame]

        # Main rect for rendering and collision
        self.rect = self.image.get_rect(topleft=(x, y))

        # Create a mask for precise collision detection
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask from the player's current image

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
        self.bullets = []  # List to store bullets
        self.bullet_cooldown = 0  # Cooldown timer for firing bullets
        self.ammo_count = 20  # Start with 20 bullets

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
                self.current_frame += self.death_animation_speed  # Use slower speed for death animation
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
                self.is_firing = False  # Reset firing state after animation finishes
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

    def play_death_animation(self):
        """
        Play the player's death animation frame by frame.
        """
        if not self.death_animation_done:
            self.death_animation_timer += self.death_animation_speed
            if self.death_animation_timer >= 1:  # Update frame only when timer reaches 1
                self.death_animation_timer = 0  # Reset the timer
                self.death_animation_frame += 1  # Move to the next frame

            if self.death_animation_frame < len(self.frames_dead):
                self.image = self.frames_dead[self.death_animation_frame]
            else:
                self.death_animation_done = True  # Mark animation as complete

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
        """
        Apply gravity to the player and ensure it falls when there is no platform beneath it.
        Prevent teleportation to the top of platforms when on the edge.
        :param platforms: A list or group of platform objects.
        """
        self.velocity_y += self.gravity  # Increase velocity due to gravity
        self.rect.y += self.velocity_y  # Move the player vertically

        # Check for collisions with platforms
        for platform in platforms:
            if platform.check_collision(self.mask, self.rect):
                if self.velocity_y > 0:  # Falling down
                    # Ensure the player is above the platform before stopping the fall
                    if self.rect.bottom - self.velocity_y <= platform.rect.top:
                        self.rect.bottom = platform.rect.top  # Stop at the top of the platform
                        self.velocity_y = 0  # Reset vertical velocity
                        self.jumping = False  # Reset jumping state

    def take_damage(self, amount, enemy_rect=None):
        """
        Reduce the player's health by the given amount.
        :param amount: The amount of damage to deal.
        :param enemy_rect: The rect of the enemy dealing the damage (optional).
        """
        if self.is_dead:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_dead = True

    def shoot(self):
        if self.bullet_cooldown == 0 and self.ammo_count > 0:  # Only shoot if cooldown is 0 and ammo is available
            direction = -1 if self.flipped else 1  # Determine the direction of the bullet

            # Calculate the bullet's starting position based on the shooting animation
            if self.flipped:
                bullet_x = self.rect.right - 83  # Adjust for flipped orientation
            else:
                bullet_x = self.rect.left + 83  # Normal orientation

            bullet_y = self.rect.top + 90  # Vertical position relative to the animation

            # Create and add the bullet
            self.bullets.append(Bullet(bullet_x, bullet_y, direction))
            self.bullet_cooldown = 20  # Set cooldown (adjust this value for firing rate)
            self.ammo_count -= 1  # Decrease ammo count

            # Play the shooting sound
            Player.shooting_sound.play()

            # Trigger the firing animation
            self.is_firing = True
            self.current_frame = 0  # Reset the animation frame

    def reload(self, amount):
        self.bullet_cooldown = max(self.bullet_cooldown - amount, 0)
        print(f"Reloaded! Cooldown now: {self.bullet_cooldown}")

    def update(self):
        if not self.is_dead:
            self.animate()  # Update the animation state
            self.update_bullets()  # Update bullets
        else:
            if self.animate():  # Play death animation
                print("Player death animation complete!")

    def update_bullets(self):
        for bullet in self.bullets[:]:  # Iterate over a copy of the list
            bullet.update()
            if bullet.rect.right < 0 or bullet.rect.left > self.screen_width or bullet.rect.top > 640:
                self.bullets.remove(bullet)  # Remove bullets that go off-screen

        # Decrease the cooldown timer
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1

    def draw(self, screen):
        # Draw the player
        screen.blit(self.image, self.rect.topleft)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

    def draw_health_bar(self, screen, position=(10, 10)):
        """
        Draw the player's health bar at the specified position.
        :param screen: The Pygame screen to draw on.
        :param position: Tuple (x, y) for the top-left corner of the health bar.
        """
        bar_width = 100  # Width of the health bar
        bar_height = 10  # Height of the health bar
        bar_x, bar_y = position

        # Calculate the health ratio
        health_ratio = self.health / 100

        # Draw the background of the health bar (gray)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Draw the foreground of the health bar (green)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def draw_ammo_count(self, screen, position=(10, 30)):
        """
        Draw the player's ammo count at the specified position.
        :param screen: The Pygame screen to draw on.
        :param position: Tuple (x, y) for the top-left corner of the ammo count.
        """
        font = pygame.font.Font(None, 24)  # Use a default font with size 24
        ammo_text = f"Ammo: {self.ammo_count}"
        text_surface = font.render(ammo_text, True, (255, 255, 255))  # White text
        screen.blit(text_surface, position)

    def draw_score(self, screen, score, position=(10, 50)):
        """
        Draw the player's score at the specified position.
        :param screen: The Pygame screen to draw on.
        :param score: The player's current score.
        :param position: Tuple (x, y) for the top-left corner of the score display.
        """
        font = pygame.font.Font(None, 24)  # Use a default font with size 24
        score_text = f"Score: {score}"
        text_surface = font.render(score_text, True, (255, 255, 255))  # White text
        screen.blit(text_surface, position)