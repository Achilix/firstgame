import pygame

# Initialize the mixer for sound effects
pygame.mixer.init()

# Load the reload sound
reload_sound = pygame.mixer.Sound("assets/reload.mp3")

class Ammo:
    def __init__(self, x, y, image_path, tile_size):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))  # Scale to TILE_SIZE
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player):
        if not self.collected:
            # Calculate the offset between the player and the ammo
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y

            # Check for pixel-perfect collision using masks
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                self.collected = True
                player.ammo_count += 10  # Increase the player's ammo count by 10
                if player.ammo_count > 20:  # Cap the ammo count at 20
                    player.ammo_count = 20
                reload_sound.play()  # Play the reload sound