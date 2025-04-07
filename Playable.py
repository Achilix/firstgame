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
                tile_x = x * TILE_SIZE  # Adjust for scrolling
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
        quit_text = font.render("Press Q to Return to Menu", True, WHITE)

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
                if event.key == pygame.K_q:  # Return to the level menu
                    return "menu"


def death_menu(score):
    """
    Display a menu when the player dies, showing the score and options to restart or quit.
    :param score: The player's score to display.
    """
    print("Entering death menu...")  # Debugging print
    font = pygame.font.Font(None, 50)  # Default font with size 50
    menu_running = True

    while menu_running:
        screen.fill(BLACK)  # Fill the screen with black for the death menu

        # Render the death menu text
        death_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {score:.2f}%", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        quit_text = font.render("Press Q to Quit to Menu", True, WHITE)

        # Center the text on the screen
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

        # Draw the text
        screen.blit(death_text, death_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()  # Update the display
        print("Death menu displayed.")  # Debugging print

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting game from death menu.")  # Debugging print
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the level
                    print("Restarting level...")  # Debugging print
                    return "restart"
                if event.key == pygame.K_q:  # Quit to menu
                    print("Quitting to menu...")  # Debugging print
                    return "menu"


# Ensure the camera system allows movement across the entire level width
class Camera:
    def __init__(self, width, height, level_width):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.level_width = level_width

    def update(self, target_rect):
        # Center the camera on the target, constrained within level bounds
        self.offset_x = max(0, min(target_rect.centerx - self.width // 2, self.level_width - self.width))
        self.offset_y = 0  # Keep the vertical offset fixed for a side-scrolling game

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)


# Refine the draw_background function to ensure seamless background coverage to the right
def draw_background(camera, level_width):
    for x in range(0, max(level_width, SCREEN_WIDTH) + background_width, background_width):
        for y in range(0, SCREEN_HEIGHT + background_height, background_height):
            screen.blit(background, camera.apply(pygame.Rect(x, y, background_width, background_height)))


def draw_zombie_score(screen, score, position=(10, 10)):
    """
    Draw the percentage of zombies killed on the screen.
    :param screen: The Pygame screen to draw on.
    :param score: The percentage of zombies killed.
    :param position: Tuple (x, y) for the top-left corner of the score display.
    """
    font = pygame.font.Font(None, 24)  # Use a default font with size 24
    score_text = f"Zombies Killed: {score:.2f}%"
    text_surface = font.render(score_text, True, (255, 255, 255))  # White text
    screen.blit(text_surface, position)


# Main game loop
def main(level_file):
    world_data = load_level(level_file)
    if not world_data:
        return

    # Calculate the level's width and height based on the tile map
    level_width = len(world_data[0]) * TILE_SIZE if world_data else SCREEN_WIDTH  # Total width of the level based on tiles
    level_height = len(world_data) * TILE_SIZE

    # Initialize objects
    player_start_x, player_start_y = 100, 500  # Default position
    enemies = []
    ammo_items = []
    bandages = []
    blocks = pygame.sprite.Group()
    door = None  # Initialize the door object
    total_zombies = 0  # Count the total number of zombies in the level

    # Parse the level data
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile <= 9:  # Block tiles (0.png to 9.png)
                blocks.add(Block(x * TILE_SIZE, y * TILE_SIZE, block_images[tile]))
            elif tile == 12:  # Player start position
                player_start_x, player_start_y = x * TILE_SIZE, y * TILE_SIZE
            elif tile == 13:  # Enemy start position
                enemies.append(Enemy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None))
                total_zombies += 1  # Increment the total zombie count
            elif tile == 10:  # Ammo
                ammo_items.append(Ammo(x * TILE_SIZE, y * TILE_SIZE, "assets/10.png", TILE_SIZE))
            elif tile == 11:  # Bandage
                bandages.append(Bandage(x * TILE_SIZE, y * TILE_SIZE, "assets/11.png", TILE_SIZE))
            elif tile == 14:  # Door (finish line)
                door = Door(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, "assets/14.png")

    # Create the player object
    player = Player(x=player_start_x, y=player_start_y, player_sprite=None, screen_width=SCREEN_WIDTH)
    player.speed = 2  # Set the player's speed to a slower value

    # Initialize the camera
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width)

    running = True
    score = 0  # Initialize the score

    while running:
        screen.fill(GREEN)  # Clear the screen

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:  # Pause the game with 'P' or 'ESC'
                    action = pause_menu()
                    if action == "menu":  # Return to the level menu
                        return

        # Get key presses
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Update player movement
        if keys[pygame.K_LEFT]:
            if player.rect.left > 0:
                player.rect.x -= player.speed

        if keys[pygame.K_RIGHT]:
            if player.rect.right < level_width:
                player.rect.x += player.speed

        # Update the camera to follow the player
        camera.update(player.rect)

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

            enemy.move_toward_player(player, blocks)  # Pass blocks for collision detection and ground check
            enemy.animate()  # Animate the enemy

        # Calculate the score as the percentage of zombies killed
        zombies_killed = total_zombies - len(enemies)  # Zombies killed = total zombies - remaining zombies
        score = (zombies_killed / total_zombies) * 100 if total_zombies > 0 else 0

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
            # Display the score and handle the level end
            print(f"Level Complete! Score: {score:.2f}%")
            next_level = "level1_data.csv"  # Replace with the actual next level file
            action = door.handle_level_end(screen, score, next_level=next_level if os.path.exists(f"LVLS/{next_level}") else None)

            if action == "next":
                main(next_level)  # Load the next level
                return
            elif action == "menu":
                return  # Exit to the level menu

        # Check if the player is killed
        if player.health <= 0:
            print("Game Over! The player has been killed.")
            if not player.death_animation_done:  # Check if the death animation is complete
                player.play_death_animation()  # Trigger the death animation
                player.animate()  # Update the animation frame

                # Redraw the current game state without clearing the screen
                draw_background(camera, level_width)
                for block in blocks:
                    screen.blit(block.image, camera.apply(block.rect))
                for enemy in enemies:
                    enemy.draw(screen, camera)
                if door:
                    door.draw(screen, camera)
                for ammo in ammo_items:
                    screen.blit(ammo.image, camera.apply(ammo.rect))
                for bandage in bandages:
                    screen.blit(bandage.image, camera.apply(bandage.rect))
                screen.blit(player.image, camera.apply(player.rect))  # Draw the player
                player.draw_ammo_count(screen)
                player.draw_health_bar(screen)
                player.draw_score(screen, score, position=(10, 50))
                draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))

                pygame.display.flip()  # Update the display
                clock.tick(60)  # Cap the frame rate
                continue  # Wait for the next frame

            # Add an additional second of wait after the animation
            for _ in range(60):  # Wait for 1 second (60 frames at 60 FPS)
                draw_background(camera, level_width)
                for block in blocks:
                    screen.blit(block.image, camera.apply(block.rect))
                for enemy in enemies:
                    enemy.draw(screen, camera)
                if door:
                    door.draw(screen, camera)
                for ammo in ammo_items:
                    screen.blit(ammo.image, camera.apply(ammo.rect))
                for bandage in bandages:
                    screen.blit(bandage.image, camera.apply(bandage.rect))
                screen.blit(player.image, camera.apply(player.rect))  # Draw the player
                player.draw_ammo_count(screen)
                player.draw_health_bar(screen)
                player.draw_score(screen, score, position=(10, 50))
                draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))

                pygame.display.flip()  # Update the display
                clock.tick(60)  # Cap the frame rate

            # Show the death menu after the animation and delay
            action = death_menu(score)
            if action == "restart":
                main(level_file)  # Restart the level
                return  # Exit the current game loop
            elif action == "menu":
                return  # Exit to the menu

        # Check if the player falls off the map
        if player.rect.top > SCREEN_HEIGHT:
            print("Game Over! The player has fallen off the map.")
            action = death_menu(score)  # Show the death menu
            if action == "restart":
                main(level_file)  # Restart the level
                return  # Exit the current game loop
            elif action == "menu":
                return  # Exit to the menu

        # Draw the repeated background
        draw_background(camera, level_width)

        # Replace scroll-based rendering with camera-based rendering
        for block in blocks:
            screen.blit(block.image, camera.apply(block.rect))

        for enemy in enemies:
            enemy.draw(screen, camera)

        if door:
            door.draw(screen, camera)

        for ammo in ammo_items:
            screen.blit(ammo.image, camera.apply(ammo.rect))

        for bandage in bandages:
            screen.blit(bandage.image, camera.apply(bandage.rect))

        # Draw the player using the camera
        screen.blit(player.image, camera.apply(player.rect))

        # Draw the player's ammo count
        player.draw_ammo_count(screen)

        # Draw the player's health bar
        player.draw_health_bar(screen)

        # Draw the player's score in the top-left corner
        player.draw_score(screen, score, position=(10, 50))

        # Draw the zombie kill score
        draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main("level0_data.csv")