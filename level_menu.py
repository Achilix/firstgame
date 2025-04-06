import pygame
import os
from button import Button
import Playable  # Import Playable to load levels

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def create_button_centered(y_offset, text, font, button_width=300, button_height=60):
    """
    Helper function to create a centered button.
    :param y_offset: Vertical offset for the button.
    :param text: Text to display on the button.
    :param font: Font object for rendering the text.
    :param button_width: Width of the button.
    :param button_height: Height of the button.
    :return: Button object.
    """
    x = (SCREEN_WIDTH - button_width) // 2  # Center horizontally
    y = y_offset  # Vertical position
    return Button(x, y, button_width, button_height, text, font, (200, 200, 200), (100, 100, 100), BLACK)

def level_menu(screen, font):
    """
    Display the level selection menu.
    :param screen: The Pygame screen to draw on.
    :param font: Font object for rendering text.
    """
    running = True

    # Dynamically load level files from the LVLS directory
    levels = [f for f in os.listdir("LVLS") if f.endswith("_data.csv")]
    level_buttons = []

    # Create centered buttons for each level
    for i, level in enumerate(levels):
        y_offset = 150 + i * 70  # Space out buttons vertically
        button = create_button_centered(y_offset, level.replace("_data.csv", ""), font)
        level_buttons.append((button, level))

    # Create a "Back" button
    back_button = create_button_centered(SCREEN_HEIGHT - 100, "Back", font)

    while running:
        screen.fill(WHITE)

        # Render menu title
        text = font.render("Select a Level", True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Center the title
        screen.blit(text, text_rect)

        # Draw level buttons
        for button, level in level_buttons:
            if button.draw(screen):
                Playable.main(level)  # Pass the selected level to Playable
                running = False  # Exit the level menu after starting the level

        # Draw the "Back" button
        if back_button.draw(screen):
            running = False  # Exit the level menu and return to the main menu

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to the start menu

        pygame.display.update()
