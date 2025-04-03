import pygame
import os
import csv
from Characters.player import Player
from Characters.Enemy import Enemy
from Ammo import Ammo
from Bandage import Bandage
from blocks import Block

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

# Load block images
block_images = []
for i in range(10):  # Images from 0.png to 9.png
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    block_images.append(img)

ammo_image_path = 'assets/10.png'
bandage_image_path = 'assets/11.png'


# Load level data from CSV
def load_level(level_file):
    world_data = []
    try:
        # Construct the full path to the level file
        level_path = os.path.join("LVLS", level_file)
        print(f"Attempting to load level file: {level_path}")  # Debugging print

        # Open and read the CSV file
        with open(level_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                world_data.append([int(tile) for tile in row if tile.strip()])  # Ensure valid integers
    except FileNotFoundError:
        print(f"Error: Level file {level_file} does not exist.")
        return None
    except ValueError as e:
        print(f"Error: Invalid data in level file {level_file}: {e}")
        return None
    return world_data


# Draw the level (optimized to only draw visible tiles)
def draw_level(world_data):
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < len(tile_images):  # Ensure the tile index is valid
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE
                if -TILE_SIZE < tile_x < SCREEN_WIDTH and -TILE_SIZE < tile_y < SCREEN_HEIGHT:
                    screen.blit(tile_images[tile], (tile_x, tile_y))


# Main game loop
def main(level_file):
    world_data = load_level(level_file)
    if not world_data:
        return

    # Initialize objects
    player_start_x, player_start_y = 100, 500  # Default position
    enemies = []
    ammo_items = []
    bandages = []
    blocks = pygame.sprite.Group()

    # Parse the level data
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile <= 9:  # Block tiles (0.png to 9.png)
                blocks.add(Block(x * TILE_SIZE, y * TILE_SIZE, block_images[tile]))
            elif tile == 12:  # Player start position
                player_start_x, player_start_y = x * TILE_SIZE, y * TILE_SIZE
            elif tile == 11:  # Enemy
                enemies.append(Enemy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None))
            elif tile == 10:  # Ammo
                ammo_items.append(Ammo(x * TILE_SIZE, y * TILE_SIZE, ammo_image_path))
            elif tile == 9:  # Bandage
                bandages.append(Bandage(x * TILE_SIZE, y * TILE_SIZE, bandage_image_path))

    # Create the player object
    player = Player(x=player_start_x, y=player_start_y, player_sprite=None, screen_width=SCREEN_WIDTH)

    running = True
    while running:
        screen.fill(GREEN)  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key presses
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Update player
        player.handle_input(keys, mouse_buttons)
        player.apply_gravity(blocks)  # Pass blocks (platforms) to apply_gravity
        player.update()

        # Check for collisions with blocks
        for block in blocks:
            if block.check_collision(player.mask, player.rect):
                # Handle collision (e.g., stop player movement or adjust position)
                if player.velocity_y > 0:  # Falling down
                    player.rect.bottom = block.rect.top
                    player.velocity_y = 0
                    player.jumping = False

        # Update enemies
        for enemy in enemies[:]:  # Iterate over a copy of the list to safely remove enemies
            if enemy.is_dead and enemy.death_animation_done:
                enemies.remove(enemy)  # Remove the enemy after the death animation is complete
                continue  # Skip further processing for this enemy

            enemy.move_toward_player(player, blocks)  # Pass blocks for collision detection
            enemy.animate()  # Animate the enemy
            enemy.draw(screen)  # Draw the enemy

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

        # Check for collisions between bullets and enemies
        for bullet in player.bullets[:]:
            for enemy in enemies:
                # Calculate the offset between the bullet and the enemy
                offset_x = enemy.rect.x - bullet.rect.x
                offset_y = enemy.rect.y - bullet.rect.y

                # Debugging: Print positions and offsets
                print(f"Bullet position: {bullet.rect.topleft}, Enemy position: {enemy.rect.topleft}")
                print(f"Offset: ({offset_x}, {offset_y})")

                # Use mask-based collision detection
                if bullet.check_collision(enemy.mask, enemy.rect):
                    print("Bullet hit enemy!")  # Debugging print
                    enemy.take_damage(20)  # Deal damage to the enemy
                    player.bullets.remove(bullet)  # Remove the bullet
                    break  # Exit the loop to avoid modifying the list during iteration

        # Check for collisions between bullets and blocks
        for bullet in player.bullets[:]:
            for block in blocks:
                # Calculate the offset between the bullet and the block
                offset_x = block.rect.x - bullet.rect.x
                offset_y = block.rect.y - bullet.rect.y

                # Use mask-based collision detection
                if bullet.check_collision(block.mask, block.rect):
                    player.bullets.remove(bullet)  # Remove the bullet on collision
                    break  # Exit the loop to avoid modifying the list during iteration

        # Visualize bullet and enemy masks
        for bullet in player.bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet.rect, 2)  # Red for bullet hitbox

        for enemy in enemies:
            pygame.draw.rect(screen, (0, 255, 0), enemy.rect, 2)  # Green for enemy hitbox

        # Draw the level
        draw_level(world_data)

        # Draw player
        player.draw(screen)

        # Draw ammo
        for ammo in ammo_items:
            ammo.draw(screen)

        # Draw bandages
        for bandage in bandages:
            bandage.draw(screen)

        # Draw blocks
        blocks.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main("level0_data.csv")