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
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask for pixel-perfect collision
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
        Check if the player collides with the ammo using mask-based collision detection.
        :param player: The player object.
        """
        if not self.collected:
            # Calculate the offset between the player and the ammo
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y

            # Use mask-based collision detection
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                self.collected = True
                player.reload(5)  # Reload the player's ammo by 5