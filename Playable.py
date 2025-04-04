import pygame
import os
import csv
from Characters.player import Player
from Characters.Enemy import Enemy
from Ammo import Ammo
from Bandage import Bandage
from blocks import Block
from Door import Door
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
ROWS = 16  # Match lvlbuilder.py
TILE_SIZE = SCREEN_HEIGHT // ROWS

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
TILE_TYPES = 14  # Number of tile types
for i in range(TILE_TYPES):
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_images.append(img)

# Load block images
block_images = []
for i in range(10):  # Images from 0.png to 9.png
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))  # Scale to TILE_SIZE
    block_images.append(img)

ammo_image_path = 'assets/10.png'
bandage_image_path = 'assets/11.png'

# Load the background image
background = pygame.image.load("assets/single_background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH + 300, SCREEN_HEIGHT + 100))  # Match lvlbuilder.py
background_width = background.get_width()
background_height = background.get_height()

scroll = 0  # Horizontal scroll offset
scroll_speed = 10  # Speed of scrolling

SCROLL_MULTIPLIER = 1.5  # Adjust this value to control the scroll speed

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
                tile_x = x * TILE_SIZE - scroll  # Adjust for scrolling
                tile_y = y * TILE_SIZE
                screen.blit(tile_images[tile], (tile_x, tile_y))


def pause_menu():
    paused = True
    font = pygame.font.Font(None, 50)  # Default font with size 50

    while paused:
        screen.fill(BLACK)  # Fill the screen with black for the pause menu

        # Render the pause menu text
        pause_text = font.render("Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, WHITE)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        # Center the text on the screen
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(pause_text, pause_rect)
        screen.blit(resume_text, resume_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Resume the game
                    paused = False
                if event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    exit()


# Main game loop
def main(level_file):
    global scroll  # Declare scroll as global to use the global variable
    world_data = load_level(level_file)
    if not world_data:
        return

    # Calculate the level's width and height based on the tile map
    level_width = len(world_data[0]) * TILE_SIZE
    level_height = len(world_data) * TILE_SIZE

    
    # Initialize objects
    player_start_x, player_start_y = 100, 500  # Default position
    enemies = []
    ammo_items = []
    bandages = []
    blocks = pygame.sprite.Group()
    door = None  # Initialize the door object

    # Parse the level data
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile <= 9:  # Block tiles (0.png to 9.png)
                blocks.add(Block(x * TILE_SIZE, y * TILE_SIZE, block_images[tile]))
            elif tile == 12:  # Player start position
                player_start_x, player_start_y = x * TILE_SIZE, y * TILE_SIZE
            elif tile == 13:  # Enemy start position
                enemies.append(Enemy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None))
            elif tile == 10:  # Ammo
                ammo_items.append(Ammo(x * TILE_SIZE, y * TILE_SIZE, "assets/10.png", TILE_SIZE))
            elif tile == 11:  # Bandage
                bandages.append(Bandage(x * TILE_SIZE, y * TILE_SIZE, "assets/11.png", TILE_SIZE))
            elif tile == 14:  # Door (finish line)
                door = Door(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, "assets/14.png")

    # Create the player object
    player = Player(x=player_start_x, y=player_start_y, player_sprite=None, screen_width=SCREEN_WIDTH)
    player.speed = 2  # Set the player's speed to a slower value

    running = True
    while running:
        screen.fill(GREEN)  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game
                    pause_menu()

        # Get key presses
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Update player movement and scrolling
        if keys[pygame.K_LEFT]:
            # Scroll the level to the left
            if scroll > 0:  # Ensure we don't scroll past the left edge
                scroll -= player.speed * SCROLL_MULTIPLIER  # Increase scroll speed
            # Move the player if they are not at the left edge of the screen
            if player.rect.left > 0:
                player.rect.x -= player.speed

        if keys[pygame.K_RIGHT]:
            # Scroll the level to the right
            if scroll < level_width - SCREEN_WIDTH:  # Ensure we don't scroll past the right edge
                scroll += player.speed * SCROLL_MULTIPLIER  # Increase scroll speed
            # Move the player if they are not at the right edge of the screen
            if player.rect.right < SCREEN_WIDTH:
                player.rect.x += player.speed

        # Clamp the scroll value
        scroll = max(0, min(scroll, level_width - SCREEN_WIDTH))

        # Update player
        player.handle_input(keys, mouse_buttons)
        player.apply_gravity(blocks)  # Pass blocks (platforms) to apply_gravity
        player.update()

        # Update bullets
        player.update_bullets()

        # Check for collisions between bullets and enemies
        for bullet in player.bullets[:]:  # Iterate over a copy of the bullet list
            for enemy in enemies[:]:  # Iterate over a copy of the enemy list
                if bullet.check_collision(enemy.mask, enemy.rect):  # Check for collision
                    enemy.take_damage(20)  # Deal 20 damage to the enemy
                    player.bullets.remove(bullet)  # Remove the bullet
                    break  # Exit the loop to avoid modifying the list during iteration

        # Allow the player to move freely near the edges
         # Prevent the player from going off the right edge

        # Update the camera to follow the player

        # Debugging print for player and camera positions

        # Check for collisions with blocks
        for block in blocks:
            if block.check_collision(player.mask, player.rect):
                # Handle collision (e.g., stop player movement or adjust position)
                if player.velocity_y > 0:  # Falling down
                    player.rect.bottom = block.rect.top
                    player.velocity_y = 0
                    player.jumping = False

        # Check for collisions between the player and enemies
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):  # Bounding box collision
                offset_x = enemy.rect.x - player.rect.x
                offset_y = enemy.rect.y - player.rect.y
                if player.mask.overlap(enemy.mask, (offset_x, offset_y)):  # Pixel-perfect collision
                    player.take_damage(10, enemy.rect)  # Deal 10 damage to the player

        # Update enemies
        for enemy in enemies[:]:  # Iterate over a copy of the list to safely remove enemies
            if enemy.is_dead and enemy.death_animation_done:
                enemies.remove(enemy)  # Remove the enemy after the death animation is complete
                continue  # Skip further processing for this enemy

            enemy.move_toward_player(player, blocks)  # Pass blocks for collision detection
            enemy.animate()  # Animate the enemy

        # Check for collisions between bullets and blocks
        for bullet in player.bullets[:]:  # Iterate over a copy of the list to safely remove bullets
            for block in blocks:
                if bullet.check_collision(block.mask, block.rect):
                    player.bullets.remove(bullet)  # Remove the bullet on collision
                    break  # Exit the loop to avoid modifying the list during iteration

        # Check for collisions with ammo
        for ammo in ammo_items[:]:  # Iterate over a copy of the list to safely remove ammo
            ammo.check_collision(player)
            if ammo.collected:
                print("Ammo collected!")  # Debugging print
                ammo_items.remove(ammo)  # Remove the ammo after it is collected

        # Check for collisions with bandages
        for bandage in bandages[:]:  # Iterate over a copy of the list to safely remove bandages
            bandage.check_collision(player)
            if bandage.collected:
                bandages.remove(bandage)  # Remove the bandage after it is collected

        # Check if the player reaches the door
        if door and door.check_collision(player.mask, player.rect):
            # Calculate the score as the percentage of zombies killed
            total_zombies = len(enemies) + len([enemy for enemy in enemies if enemy.is_dead])
            zombies_killed = len([enemy for enemy in enemies if enemy.is_dead])
            score = (zombies_killed / total_zombies) * 100 if total_zombies > 0 else 0

            # Display the score and end the level
            print(f"Level Complete! Score: {score:.2f}%")
            running = False  # Exit the game loop

        # Draw the repeated background
        for x in range(0, level_width, background_width):
            for y in range(0, level_height, background_height):
                screen.blit(background, (x - scroll, y))

        # Draw blocks
        for block in blocks:
            screen.blit(block.image, (block.rect.x - scroll, block.rect.y))

        # Draw enemies and their health bars
        for enemy in enemies:
            enemy.draw(screen)

        # Draw ammo
        for ammo in ammo_items:
            screen.blit(ammo.image, (ammo.rect.x - scroll, ammo.rect.y))

        # Draw bandages
        for bandage in bandages:
            screen.blit(bandage.image, (bandage.rect.x - scroll, bandage.rect.y))

        # Draw the door
        if door:
            door.draw(screen, scroll)

        # Draw bullets
        for bullet in player.bullets:
            bullet.draw(screen)
            bullet_x, bullet_y = bullet.rect.x, bullet.rect.y
            print(f"Bullet created at ({bullet_x}, {bullet_y})")

        # Draw the player
        screen.blit(player.image, (player.rect.x, player.rect.y))  # Player stays fixed

        # Draw the player's ammo count
        player.draw_ammo_count(screen)

        # Draw the player's health bar
        player.draw_health_bar(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main("level0_data.csv")