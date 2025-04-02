import pygame
import csv
from Characters.player import Player
from Characters.Enemy import Enemy
from Ammo import Ammo
from Bandage import Bandage

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
TILE_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 201, 120)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Playable Level")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
tile_images = []
TILE_TYPES = 11  # Number of tile types
for i in range(TILE_TYPES):
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_images.append(img)

ammo_image_path = 'assets/10.png'
bandage_image_path = 'assets/11.png'

# Load level data from CSV
def load_level(level):
    world_data = []
    try:
        with open(f'LVLS/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                world_data.append([int(tile) for tile in row])
    except FileNotFoundError:
        print(f"Error: Level {level} does not exist.")
        return None
    return world_data

# Draw the level
def draw_level(world_data):
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < len(tile_images):  # Ensure the tile index is valid
                screen.blit(tile_images[tile], (x * TILE_SIZE, y * TILE_SIZE))
            else:
                print(f"Invalid tile index {tile} at position ({x}, {y})")

# Main game loop
def main():
    level = 0  # Start with level 0
    world_data = load_level(level)
    if not world_data:
        return

    # Create player and enemy objects
    player = Player(x=100, y=500, player_sprite=None, screen_width=SCREEN_WIDTH)  # No static sprite
    enemies = []
    ammo_items = []
    bandages = []

    # Parse the level data to place enemies, ammo, and bandages
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile == 1:  # Example: Tile 1 is the player start position
                player.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
            elif tile == 2:  # Example: Tile 2 is an enemy
                enemies.append(Enemy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None))  # No static sprite
            elif tile == 3:  # Example: Tile 3 is ammo
                ammo_items.append(Ammo(x * TILE_SIZE, y * TILE_SIZE, ammo_image_path))
            elif tile == 4:  # Example: Tile 4 is a bandage
                bandages.append(Bandage(x * TILE_SIZE, y * TILE_SIZE, bandage_image_path))

    running = True
    while running:
        screen.fill(GREEN)  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key presses
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()  # Get mouse button states

        # Update player
        player.handle_input(keys, mouse_buttons)  # Pass mouse_buttons here
        player.apply_gravity([])
        player.update()

        # Update enemies
        for enemy in enemies:
            enemy.move_toward_player(player)
            if player.rect.colliderect(enemy.rect):
                player.take_damage(10, enemy)

        # Check for collisions with ammo
        for ammo in ammo_items[:]:
            ammo.check_collision(player)
            if ammo.collected:
                ammo_items.remove(ammo)

        # Check for collisions with bandages
        for bandage in bandages[:]:
            bandage.check_collision(player)
            if bandage.collected:
                bandages.remove(bandage)

        # Draw the level
        draw_level(world_data)

        # Draw player
        player.draw(screen)

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Draw ammo
        for ammo in ammo_items:
            ammo.draw(screen)

        # Draw bandages
        for bandage in bandages:
            bandage.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()