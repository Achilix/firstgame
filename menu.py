import pygame
import os
import subprocess  # To run the Level Builder script
from button import Button
import Playable  # Import Playable to load levels

# Initialize pygame
pygame.init()

# Initialize the mixer for background music
pygame.mixer.init()
pygame.mixer.music.load("assets/backgroundsong.mp3")  # Load the background song
pygame.mixer.music.set_volume(0.5)  # Set initial volume
pygame.mixer.music.play(-1)  # Play the song in a loop

# Variable to track mute state
is_muted = False

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Load the PressStart2P font
font_path = "PressStart2P.ttf"  # Path to the font file
font = pygame.font.Font(font_path, 20)  # Set the font size to 20

# Load and scale the single background image
background_image = pygame.image.load("assets/single_background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Variables for scrolling background (global for both menus)
bg_positions = [(i * SCREEN_WIDTH, 0) for i in range(2)]  # Two instances for seamless scrolling
scroll_speed = 0.5  # Reduced scroll speed for smoother and slower scrolling

# Function to render the scrolling background with fog
def render_background():
    global bg_positions

    # Scroll the background
    bg_positions = [(x - scroll_speed, y) for x, y in bg_positions]

    # Reset positions when an image goes off-screen
    if bg_positions[0][0] <= -SCREEN_WIDTH:
        bg_positions.pop(0)  # Remove the first image
        new_x = bg_positions[-1][0] + SCREEN_WIDTH  # Position the new image after the last one
        bg_positions.append((new_x, 0))  # Add a new image at the end

    # Draw the background images
    for x, y in bg_positions:
        screen.blit(background_image, (x, y))

    # Add white fog effect
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fog_surface.fill((255, 255, 255, 50))  # Semi-transparent white
    screen.blit(fog_surface, (0, 0))

# Function to toggle mute
def toggle_mute():
    global is_muted
    if is_muted:
        pygame.mixer.music.set_volume(0.5)  # Unmute
        is_muted = False
    else:
        pygame.mixer.music.set_volume(0)  # Mute
        is_muted = True

# Helper function to create a centered button
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
    return Button(x, y, button_width, button_height, text, font, GRAY, DARK_GRAY, BLACK)

# Main menu function
def start_menu():
    running = True

    # Create centered buttons
    start_button = create_button_centered(200, "Start Game", font)
    lvlbuilder_button = create_button_centered(300, "Level Builder", font)
    quit_button = create_button_centered(400, "Quit", font)

    while running:
        render_background()  # Render the scrolling background with fog

        # Render menu title
        title_font = pygame.font.Font(font_path, 30)  # Larger font size for the title
        title_text = title_font.render("Zombie Survival", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Center the title
        screen.blit(title_text, title_rect)

        # Render mute instructions
        mute_text = font.render("Press M to Mute/Unmute Music", True, BLACK)
        mute_rect = mute_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(mute_text, mute_rect)

        # Draw buttons
        if start_button.draw(screen):
            level_menu()  # Go to the level selection menu
        if lvlbuilder_button.draw(screen):
            run_lvlbuilder()  # Launch the Level Builder
        if quit_button.draw(screen):
            running = False  # Exit the game

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Toggle mute
                    toggle_mute()

        pygame.display.update()

# Function to run the Level Builder
def run_lvlbuilder():
    try:
        # Run the Level Builder script
        subprocess.run(["python", "LVLBUILDER/lvlbuilder.py"])
    except FileNotFoundError:
        print("Error: Level Builder script not found.")

# Level selection menu
def level_menu():
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
        render_background()  # Render the scrolling background with fog

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

# Run the start menu
start_menu()
pygame.quit()