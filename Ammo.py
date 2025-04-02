import pygame

class Ammo:
    def __init__(self, x, y, image_path):
        """
        Initialize the ammo object.
        :param x: The x-coordinate of the ammo.
        :param y: The y-coordinate of the ammo.
        :param image_path: Path to the ammo image.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the image if needed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False  # Track if the ammo has been collected

    def draw(self, screen):
        """
        Draw the ammo on the screen.
        :param screen: The Pygame screen surface.
        """
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player):
        """
        Check if the player collides with the ammo.
        :param player: The player object.
        """
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            player.reload(10)  # Add 10 bullets to the player's bullet count