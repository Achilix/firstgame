import pygame

class Bullet:
    def __init__(self, x, y, direction):
        # Create the bullet image
        self.image = pygame.Surface((5, 5))  # Small black dot (5x5)
        self.image.fill((0, 0, 0))  # Black color for the bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction  # Speed depends on direction (-1 for left, 1 for right)

        # Create a mask for precise collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Move the bullet horizontally
        self.rect.x += self.speed

    def check_collision(self, other_mask, other_rect):
        # Calculate the offset between the bullet and the other object
        offset_x = other_rect.x - self.rect.x
        offset_y = other_rect.y - self.rect.y

        # Check for pixel-perfect collision using masks
        return self.mask.overlap(other_mask, (offset_x, offset_y)) is not None

    def draw(self, screen):
        # Draw the bullet on the screen
        screen.blit(self.image, self.rect)
        # Visualize the bullet's mask bounding rectangle
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red for the bullet's hitbox