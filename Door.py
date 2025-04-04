import pygame

class Door:
    def __init__(self, x, y, tile_size, image_path):
        """
        Initialize the Door object.
        :param x: X-coordinate of the door.
        :param y: Y-coordinate of the door.
        :param tile_size: Size of the tile (width and height).
        :param image_path: Path to the door image.
        """
        self.rect = pygame.Rect(x, y, tile_size, tile_size)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))  # Scale to TILE_SIZE
        self.mask = pygame.mask.from_surface(self.image)  # Create a mask from the image

    def draw(self, screen, scroll):
        """
        Draw the door on the screen.
        :param screen: The Pygame screen to draw on.
        :param scroll: The horizontal scroll offset.
        """
        screen.blit(self.image, (self.rect.x - scroll, self.rect.y))

    def check_collision(self, player_mask, player_rect):
        """
        Check if the player's mask collides with the door's mask.
        :param player_mask: The player's mask.
        :param player_rect: The player's rectangle.
        :return: True if the player collides with the door, False otherwise.
        """
        offset_x = self.rect.x - player_rect.x
        offset_y = self.rect.y - player_rect.y
        return player_mask.overlap(self.mask, (offset_x, offset_y)) is not None