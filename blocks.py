import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self, scroll):
        # Update block position based on scroll
        self.rect.x -= scroll

    def check_collision(self, player_rect):
        # Check for collision with the player
        return self.rect.colliderect(player_rect)
