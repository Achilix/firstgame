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

    def draw(self, screen, camera):
        """
        Draw the door on the screen using the camera offset.
        :param screen: The Pygame screen to draw on.
        :param camera: The camera object to apply the offset.
        """
        screen.blit(self.image, camera.apply(self.rect))

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

    def handle_level_end(self, screen, score, next_level=None):
        """
        Display the score and handle the transition to the next level or level menu.
        :param screen: The Pygame screen to draw on.
        :param score: The player's score to display.
        :param next_level: The next level file to load. If None, return to the level menu.
        """
        font = pygame.font.Font(None, 50)  # Default font with size 50
        running = True

        while running:
            screen.fill((0, 0, 0))  # Black background

            # Render the level end text
            level_complete_text = font.render("Level Complete!", True, (255, 255, 255))
            score_text = font.render(f"Score: {score:.2f}%", True, (255, 255, 255))
            next_text = font.render("Press N for Next Level", True, (255, 255, 255))
            menu_text = font.render("Press M for Level Menu", True, (255, 255, 255))

            # Center the text on the screen
            level_complete_rect = level_complete_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            next_rect = next_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            menu_rect = menu_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

            # Draw the text
            screen.blit(level_complete_text, level_complete_rect)
            screen.blit(score_text, score_rect)
            screen.blit(next_text, next_rect)
            screen.blit(menu_text, menu_rect)

            pygame.display.flip()  # Update the display

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n and next_level:  # Load the next level
                        print(f"Next level requested: {next_level}")  # Debugging message
                        return "next"
                    if event.key == pygame.K_m:  # Return to the level menu
                        return "menu"