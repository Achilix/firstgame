import pygame

class Bandage:
    def __init__(self, x, y, image_path, tile_size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player):
        if not self.collected:
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                self.collected = True
                player.health += 50
                if player.health > 100:
                    player.health = 100