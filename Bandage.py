import pygame

class Bandage:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize if needed
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)

    def check_collision(self, player):
        """
        Check if the player collides with the bandage using mask-based collision detection.
        :param player: The player object.
        """
        if not self.collected:
            # Calculate the offset between the player and the bandage
            offset_x = player.rect.x - self.rect.x
            offset_y = player.rect.y - self.rect.y

            # Debugging: Print positions and offsets
            print(f"Player position: {player.rect.topleft}, Bandage position: {self.rect.topleft}")
            print(f"Offset: ({offset_x}, {offset_y})")

            # Use mask-based collision detection
            if self.mask.overlap(player.mask, (offset_x, offset_y)):
                self.collected = True
                player.health += 50  # Increase the player's health by 50
                if player.health > 100:  # Cap the player's health at 100
                    player.health = 100
                print(f"Player picked up bandage! Health: {player.health}")