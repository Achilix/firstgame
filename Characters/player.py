import pygame
import random

class Player:
    def __init__(self, x, y, player_sprite, screen_width):
        self.image = player_sprite
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.jump_height = 10
        self.flipped = False
        self.screen_width = screen_width  # Store screen width for boundary checks
        self.health = 100  # Player's health (out of 100)
        self.knockback_force = 5  # Knockback distance per frame
        self.knockback_frames = 10  # Number of frames for knockback animation
        self.knockback_direction = 0  # Direction of knockback (-1 for left, 1 for right)
        self.knockback_timer = 0  # Timer for knockback animation
        self.knockback_source = None  # Store the zombie's rectangle causing the knockback
        self.invincible = False  # Whether the player is invincible
        self.invincibility_timer = 0  # Timer for invincibility
        self.gun = None  # Placeholder for the gun object

    def handle_movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            if not self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False
        if keys[pygame.K_UP] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height

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
        if not self.invincible:  # Only take damage if not invincible
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                print("Player is dead!")
            else:
                self.knockback_direction = knockback_direction
                self.knockback_timer = self.knockback_frames  # Start knockback animation
                self.knockback_source = zombie_rect  # Store the zombie's rectangle
                self.invincible = True  # Make the player invincible
                self.invincibility_timer = 60  # Set invincibility duration (e.g., 1 second at 60 FPS)

    def knockback(self):
        """
        Apply knockback to the player over multiple frames, ensuring it moves away from the zombie.
        """
        if self.knockback_timer > 0 and self.knockback_source:
            # Determine the knockback direction based on the zombie's position
            if self.rect.centerx < self.knockback_source.centerx:
                self.knockback_direction = -1  # Move left if the player is to the left of the zombie
            else:
                self.knockback_direction = 1  # Move right if the player is to the right of the zombie

            # Apply knockback gradually
            self.rect.x += self.knockback_force * self.knockback_direction
            self.knockback_timer -= 1

            # Ensure the player doesn't go out of bounds
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.screen_width:
                self.rect.right = self.screen_width

    def update(self):
        """
        Update the player's state (e.g., invincibility timer, knockback animation).
        """
        if self.invincible:
            self.invincibility_timer -= 1
            if self.invincibility_timer <= 0:
                self.invincible = False  # End invincibility

        # Handle knockback animation
        self.knockback()

        # Update gun position
        if self.gun:
            self.gun.update_position(self.rect, self.flipped)
            self.gun.update_bullets()

    def draw(self, screen):
        # Draw the player sprite
        screen.blit(self.image, self.rect.topleft)

        # Draw the health bar
        # Red background (full health bar)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        # Green foreground (current health)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))

    def grabcoin(self, coin, score):
        if self.rect.colliderect(coin.rect):
            score.update()
            print("Coin collected")
            coin.rect.x = random.randint(0, self.screen_width - coin.rect.width)
            coin.rect.y = random.randint(0, 500)  # Adjust Y position as needed
            return True
        return False

    def equip_gun(self, gun):
        """
        Equip a gun to the player.
        :param gun: The gun object to equip.
        """
        self.gun = gun