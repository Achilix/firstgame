import pygame
import os
from button import Button
import Playable  # Import Playable to load levels

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Fonts
pixel_font = pygame.font.Font("PressStart2P.ttf", 20)

# Buttons
start_button = Button(300, 200, 200, 50, "Start Game", pixel_font, GRAY, DARK_GRAY, BLACK)
about_button = Button(300, 300, 200, 50, "About Us", pixel_font, GRAY, DARK_GRAY, BLACK)

def start_menu():
    running = True
    while running:
        screen.fill(WHITE)

        # Draw buttons
        if start_button.draw(screen):
            level_menu()
        if about_button.draw(screen):
            about_us()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

def level_menu():
    running = True

    # Dynamically load level files from the LVLS directory
    levels = [f for f in os.listdir("LVLS") if f.endswith("_data.csv")]
    level_buttons = []

    # Create buttons for each level
    for i, level in enumerate(levels):
        button = Button(300, 100 + i * 60, 200, 50, level.replace("_data.csv", ""), pixel_font, GRAY, DARK_GRAY, BLACK)
        level_buttons.append((button, level))

    while running:
        screen.fill(WHITE)
        text = pixel_font.render("Select a Level", True, BLACK)
        screen.blit(text, (250, 50))

        # Draw level buttons
        for button, level in level_buttons:
            if button.draw(screen):
                Playable.main(level)  # Pass the selected level to Playable
                running = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to the start menu

        pygame.display.update()

def about_us():
    running = True
    while running:
        screen.fill(WHITE)

        # Render the "About Us" text from the README
        about_text = [
            "About Us:",
            "This is a 2D game where the player",
            "must survive against zombies while",
            "navigating the environment.",
            "",
            "Goal: Survive as long as possible",
            "while managing resources and",
            "avoiding enemies.",
        ]

        y_offset = 100
        for line in about_text:
            text = pixel_font.render(line, True, BLACK)
            screen.blit(text, (50, y_offset))
            y_offset += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to the start menu

        pygame.display.update()

# Run the start menu
start_menu()
pygame.quit()