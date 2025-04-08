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
    running = True

    # Load a background image
    background = pygame.image.load(r"assets\single_background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load the PressStart2P font
    press_start_font_path = r"PressStart2P.ttf"  # Update the path if needed
    title_font = pygame.font.Font(press_start_font_path, 40)  # Smaller size for this font
    button_font = pygame.font.Font(press_start_font_path, 20)  # Smaller size for buttons

    # Dynamically load level files from the LVLS directory
    levels = [f for f in os.listdir("LVLS") if f.endswith("_data.csv")]

    # Create centered buttons for each level, stacked horizontally
    level_buttons = []
    button_width = 300
    button_height = 60
    padding = 20  # Space between buttons
    max_buttons_per_row = SCREEN_WIDTH // (button_width + padding)  # Calculate max buttons per row

    for i, level in enumerate(levels):
        row = i // max_buttons_per_row  # Determine the row
        col = i % max_buttons_per_row  # Determine the column
        x_offset = (col * (button_width + padding)) + (SCREEN_WIDTH - (max_buttons_per_row * (button_width + padding))) // 2
        y_offset = 150 + row * (button_height + padding)  # Space out rows vertically
        button = Button(x_offset, y_offset, button_width, button_height, level.replace("_data.csv", ""), button_font, (200, 200, 200), (100, 100, 100), BLACK)
        level_buttons.append((button, level))

    # Create a "Back" button
    back_button = create_button_centered(SCREEN_HEIGHT - 100, "Back", button_font)

    while running:
        screen.blit(background, (0, 0))  # Draw the background image

        # Render menu title
        text = title_font.render("Select a Level", True, (255, 215, 0))  # Gold color
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Center the title
        screen.blit(text, text_rect)

        # Draw level buttons
        for button, level in level_buttons:
            if button.draw(screen):
                level_path = os.path.join("LVLS", level)
                print(f"Button clicked for level: {level}")  # Debugging message
                print(f"Resolved level path: {level_path}")  # Debugging message
                Playable.main(level)
                running = False
                break  

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
