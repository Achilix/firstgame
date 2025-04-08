import pygame
import os
import subprocess
from button import Button
import Playable
from level_menu import level_menu

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets/backgroundsong.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

is_muted = False

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

font_path = "PressStart2P.ttf"
font = pygame.font.Font(font_path, 20)

background_image = pygame.image.load("assets/single_background.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg_positions = [(i * SCREEN_WIDTH, 0) for i in range(2)]
scroll_speed = 0.5

def render_background():
    global bg_positions
    bg_positions = [(x - scroll_speed, y) for x, y in bg_positions]
    if bg_positions[0][0] <= -SCREEN_WIDTH:
        bg_positions.pop(0)
        new_x = bg_positions[-1][0] + SCREEN_WIDTH
        bg_positions.append((new_x, 0))
    for x, y in bg_positions:
        screen.blit(background_image, (x, y))
    fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    fog_surface.fill((255, 255, 255, 50))
    screen.blit(fog_surface, (0, 0))

def toggle_mute():
    global is_muted
    if is_muted:
        pygame.mixer.music.set_volume(0.5)
        is_muted = False
    else:
        pygame.mixer.music.set_volume(0)
        is_muted = True

def create_button_centered(y_offset, text, font, button_width=300, button_height=60):
    x = (SCREEN_WIDTH - button_width) // 2
    y = y_offset
    return Button(x, y, button_width, button_height, text, font, GRAY, DARK_GRAY, BLACK)

def start_menu():
    running = True
    start_button = create_button_centered(200, "Start Game", font)
    lvlbuilder_button = create_button_centered(300, "Level Builder", font)
    quit_button = create_button_centered(400, "Quit", font)
    while running:
        render_background()
        title_font = pygame.font.Font(font_path, 30)
        title_text = title_font.render("Zombie Survival", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        mute_text = font.render("Press M to Mute/Unmute Music", True, BLACK)
        mute_rect = mute_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(mute_text, mute_rect)
        if start_button.draw(screen):
            level_menu(screen, font)
        if lvlbuilder_button.draw(screen):
            run_lvlbuilder()
        if quit_button.draw(screen):
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    toggle_mute()
        pygame.display.update()

def run_lvlbuilder():
    try:
        subprocess.run(["python", "LVLBUILDER/lvlbuilder.py"])
    except FileNotFoundError:
        print("Error: Level Builder script not found.")

start_menu()
pygame.quit()