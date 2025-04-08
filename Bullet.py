import pygame

class Bullet:
    def __init__(self, x, y, direction):
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10 * direction
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed

    def check_collision(self, other_mask, other_rect):
        offset_x = other_rect.x - self.rect.x
        offset_y = other_rect.y - self.rect.y
        return self.mask.overlap(other_mask, (offset_x, offset_y)) is not None

    def draw(self, screen):
        screen.blit(self.image, self.rect)