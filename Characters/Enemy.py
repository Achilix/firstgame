import pygame  # Import pygame

class Enemy:
    def __init__(self, x, y, width, height, enemy_sprite):
        self.image = pygame.transform.scale(enemy_sprite, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1  # Reduced speed to make the zombie slower
        self.flipped = False
        self.health = 100  # Zombie's health (out of 100)

    def move_toward_player(self, player):
        """
        Move the enemy toward the player's position horizontally.
        Stop moving if colliding with the player.
        :param player: The player object to chase.
        """
        # Check for collision with the player
        if self.rect.colliderect(player.rect):
            return  # Stop moving if colliding with the player

        # Move horizontally toward the player
        if self.rect.centerx < player.rect.centerx:
            self.rect.x += self.speed  # Move right
            if self.flipped:  # Flip the image to face right
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False
        elif self.rect.centerx > player.rect.centerx:
            self.rect.x -= self.speed  # Move left
            if not self.flipped:  # Flip the image to face left
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = True

        # Ensure the enemy doesn't jump or move vertically
        # The enemy's vertical position remains constant

    def take_damage(self, amount):
        """
        Reduce the enemy's health by the specified amount.
        :param amount: The amount of damage to reduce from the enemy's health.
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Enemy is dead!")

    def draw(self, screen):
        """
        Draw the enemy and its health bar.
        """
        # Draw the enemy sprite
        screen.blit(self.image, self.rect.topleft)

        # Draw the health bar
        # Red background (full health bar)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        # Green foreground (current health)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))