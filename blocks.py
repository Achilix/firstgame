import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, scroll):
        self.rect.x -= scroll

    def check_collision(self, other_mask, other_rect):
        offset_x = other_rect.x - self.rect.x
        offset_y = other_rect.y - self.rect.y
        return self.mask.overlap(other_mask, (offset_x, offset_y)) is not None
