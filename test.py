import pygame
from Characters.player import Player
from Characters.Enemy import Enemy
from button import Button
# from guns import Rifle, Pistol  # Commented out
# from GunPickup import GunPickup  # Commented out

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
player_sprite = pygame.image.load('assets/13.png').convert_alpha()  # Load player sprite
enemy_sprite = pygame.image.load('assets/14.png').convert_alpha()  # Load zombie sprite

# Resize sprites (optional, if needed)
player_sprite = pygame.transform.scale(player_sprite, (50, 50))
enemy_sprite = pygame.transform.scale(enemy_sprite, (50, 50))

# Create player and enemy objects
player = Player(x=100, y=500, player_sprite=player_sprite, screen_width=SCREEN_WIDTH)
enemy = Enemy(x=400, y=500, width=50, height=50, enemy_sprite=enemy_sprite)

# Platforms (for simplicity, just a ground platform)
platform = pygame.Rect(0, 550, SCREEN_WIDTH, 50)
platforms = [platform]

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
        # Get key presses
        keys = pygame.key.get_pressed()

        # Update player
        player.handle_movement(keys)
        player.apply_gravity(platforms)
        player.update()  # Update player state (e.g., invincibility)

        # Update enemy
        enemy.move_toward_player(player)  # Enemy chases the player

        # Check for collision between player and enemy
        if player.rect.colliderect(enemy.rect):
            print("Player hit by enemy!")
            knockback_direction = 1 if player.rect.centerx < enemy.rect.centerx else -1
            player.take_damage(10, knockback_direction, enemy.rect)  # Pass only the required arguments

        # Draw everything
        pygame.draw.rect(screen, BLACK, platform)  # Draw the ground platform
        player.draw(screen)
        enemy.draw(screen)
    else:
        # Draw the restart button
        if restart_button.draw(screen):
            player.health = 100
            player.rect.topleft = (100, 500)
            enemy.rect.topleft = (400, 500)
            print("Game restarted!")

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

def take_damage(self, amount):
    self.health -= amount
    if self.health <= 0:
        self.health = 0
        print("Enemy is dead!")