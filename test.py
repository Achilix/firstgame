import pygame
from Characters.player import Player
from Characters.Enemy import Enemy
from button import Button
from Ammo import Ammo
from Bandage import Bandage

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player and Enemy Interaction Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load assets
ammo_image_path = 'assets/10.png'  # Replace with the correct path to your ammo image
bandage_image_path = 'assets/11.png'  # Replace with the correct path to your bandage image

# Tile size
TILE_SIZE = 50

# Platforms (for simplicity, just a ground platform)
platform = pygame.Rect(0, 550, SCREEN_WIDTH, 50)
platforms = [platform]

# Create player and enemy objects
player = Player(x=100, y=platform.top - TILE_SIZE, player_sprite=None, screen_width=SCREEN_WIDTH)  # Adjusted player position
enemy = Enemy(x=400, y=500, width=50, height=50, enemy_sprite=None)  # No static sprite

# Create an ammo object
ammo = Ammo(x=300, y=520, image_path=ammo_image_path)

# Create a bandage object
bandage = Bandage(x=500, y=520, image_path=bandage_image_path)

# Font for the restart button
font = pygame.font.SysFont('Arial', 30)

# Create a restart button
restart_button = Button(
    x=SCREEN_WIDTH // 2 - 100,
    y=SCREEN_HEIGHT // 2 - 25,
    width=200,
    height=50,
    text="Restart",
    font=font,
    color=(0, 128, 0),  # Green
    hover_color=(0, 200, 0),  # Lighter green on hover
    text_color=(255, 255, 255)  # White text
)

# Game loop
running = True
while running:
    screen.fill(WHITE)  # Clear the screen

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.health > 0:
        # Normal game logic
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        # Update player
        player.handle_input(keys, mouse_buttons)
        player.apply_gravity(platforms)
        player.update()

        # Update enemy
        if enemy is not None:
            enemy.move_toward_player(player)

        # Check for collision between player and enemy
        if enemy is not None and player.rect.colliderect(enemy.rect):
            player.take_damage(10, enemy)

        # Check for bullet collisions with the enemy
        for bullet in player.bullets[:]:
            if enemy is not None and enemy.rect.colliderect(bullet.rect):
                enemy.take_damage(20)
                player.bullets.remove(bullet)

        # Animate the enemy
        if enemy is not None and enemy.animate():
            enemy = None

        # Update bullets
        for bullet in player.bullets[:]:
            bullet.update()
            bullet.draw(screen)
            if bullet.rect.right < 0 or bullet.rect.left > SCREEN_WIDTH:
                player.bullets.remove(bullet)

        # Check for collision with ammo
        ammo.check_collision(player)

        # Check for collision with bandage
        bandage.check_collision(player)

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, platform)
        player.draw(screen)
        if enemy is not None:
            enemy.draw(screen)
        ammo.draw(screen)  # Draw the ammo if it hasn't been collected
        bandage.draw(screen)  # Draw the bandage

        pygame.display.flip()
    else:
        # Handle player death
        if not player.death_animation_done:
            # Continue updating the player to play the death animation
            player.update()
            player.draw(screen)
            pygame.display.flip()
        else:
            # Show restart button or end game logic
            if restart_button.draw(screen):
                player.health = 100
                player.rect.topleft = (100, 500)
                player.is_dead = False
                player.death_animation_done = False
                enemy = Enemy(x=400, y=500, width=50, height=50, enemy_sprite=None)  # No static sprite
                print("Game restarted!")

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()