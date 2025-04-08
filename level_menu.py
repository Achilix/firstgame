import pygame
import os
from button import Button
import Playable

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def create_button_centered(y_offset, text, font, button_width=300, button_height=60):
    x = (SCREEN_WIDTH - button_width) // 2
    y = y_offset
    return Button(x, y, button_width, button_height, text, font, (200, 200, 200), (100, 100, 100), BLACK)

def level_menu(screen, font):
    running = True
    background = pygame.image.load(r"assets\single_background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    press_start_font_path = r"PressStart2P.ttf"
    title_font = pygame.font.Font(press_start_font_path, 40)
    button_font = pygame.font.Font(press_start_font_path, 20)
    levels = [f for f in os.listdir("LVLS") if f.endswith("_data.csv")]
    level_buttons = []
    button_width = 300
    button_height = 60
    padding = 20
    max_buttons_per_row = SCREEN_WIDTH // (button_width + padding)
    for i, level in enumerate(levels):
        row = i // max_buttons_per_row
        col = i % max_buttons_per_row
        x_offset = (col * (button_width + padding)) + (SCREEN_WIDTH - (max_buttons_per_row * (button_width + padding))) // 2
        y_offset = 150 + row * (button_height + padding)
        button = Button(x_offset, y_offset, button_width, button_height, level.replace("_data.csv", ""), button_font, (200, 200, 200), (100, 100, 100), BLACK)
        level_buttons.append((button, level))
    back_button = create_button_centered(SCREEN_HEIGHT - 100, "Back", button_font)
    while running:
        screen.blit(background, (0, 0))
        text = title_font.render("Select a Level", True, (255, 215, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(text, text_rect)
        for button, level in level_buttons:
            if button.draw(screen):
                level_path = os.path.join("LVLS", level)
                Playable.main(level)
                running = False
                break
        if back_button.draw(screen):
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        pygame.display.update()
