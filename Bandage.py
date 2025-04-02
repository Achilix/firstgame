import pygame

class Bandage:
    def __init__(self, x, y, image_path):
        """
        Initialize the bandage object.
        :param x: The x-coordinate of the bandage.
        :param y: The y-coordinate of the bandage.
        :param image_path: Path to the bandage image.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the image if needed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False  # Track if the bandage has been collected

    def draw(self, screen):
        """
        Draw the bandage on the screen.
        :param screen: The Pygame screen surface.
        """
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player):
        """
        Check if the player collides with the bandage.
        :param player: The player object.
        """
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            player.health += 50  # Increase the player's health by 50
            if player.health > 100:  # Cap the player's health at 100
                player.health = 100