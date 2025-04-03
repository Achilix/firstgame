import pygame

class Camera:
    def __init__(self, width, height, screen_width, screen_height):
        self.camera_rect = pygame.Rect(0, 0, width, height)  # Camera's view rectangle
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def apply(self, entity):
        """
        Adjust the position of an entity based on the camera's offset.
        :param entity: The entity to adjust (e.g., player, enemy, block).
        :return: Adjusted position.
        """
        return entity.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def apply_rect(self, rect):
        """
        Adjust a rectangle's position based on the camera's offset.
        :param rect: The rectangle to adjust.
        :return: Adjusted rectangle.
        """
        return rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update(self, target):
        """
        Update the camera's position to keep the target (player) centered.
        :param target: The target entity to follow.
        """
        x = target.rect.centerx - self.screen_width // 2
        y = target.rect.centery - self.screen_height // 2

        # Clamp the camera to the level boundaries
        x = max(0, min(x, self.width - self.screen_width))
        y = max(0, min(y, self.height - self.screen_height))

        self.camera_rect = pygame.Rect(x, y, self.width, self.height)