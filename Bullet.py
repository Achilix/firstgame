import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((5, 5))  # Small black dot (5x5)
        self.image.fill((0, 0, 0))  # Black color for the bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction  # Speed depends on direction (-1 for left, 1 for right)

    def update(self):
        self.rect.x += self.speed  # Move the bullet horizontally

    def draw(self, screen):
        screen.blit(self.image, self.rect)