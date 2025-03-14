import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
FPS = 60
GAME_DURATION = 30  # Game duration in seconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platform Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load the player sprite
player_sprite = pygame.image.load(r'assets\sprite-0001.png').convert_alpha()

# Scale the player sprite to three times its original size
player_sprite = pygame.transform.scale(player_sprite, (player_sprite.get_width() * 3, player_sprite.get_height() * 3))

# Load the enemy sprite
enemy_sprite = pygame.image.load(r'assets\sprite-0004.png').convert_alpha()

# Scale the enemy sprite to the same size as the player sprite
enemy_sprite = pygame.transform.scale(enemy_sprite, (player_sprite.get_width(), player_sprite.get_height()))

class Score:
    def __init__(self):
        self.score = 0  # Initialize the score to 0
        self.high_score = 0
        self.font = pygame.font.Font(None, 36)

    def display(self, screen):
        text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(text, (10, 10))
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        screen.blit(high_score_text, (10, 50))

    def update(self):
        self.score += 1

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.score = 0

class Player:
    def __init__(self, x, y):
        self.image = player_sprite
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.jump_height = 10
        self.flipped = False

    def handle_movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
            if not self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.flipped:
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = False
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height

    def apply_gravity(self, platforms):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Collision with the platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.bottom >= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def grabcoin(self, coin, score):
        if self.rect.colliderect(coin.rect):
            score.update()
            print("Coin collected")
            coin.rect.x = random.randint(0, SCREEN_WIDTH - coin.width)
            coin.rect.y = 500
            return True
        return False

class Enemy:
    def __init__(self, x, y, width, height):
        self.image = pygame.transform.scale(enemy_sprite, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = 1
        self.flipped = False

    def move(self, platforms):
        self.rect.x += self.speed * self.direction

        # Check for collision with platforms to change direction
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.rect.left <= platform.rect.left or self.rect.right >= platform.rect.right:
                    self.direction *= -1
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flipped = not self.flipped
                    break

        # Check for collision with the edges of the screen
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = not self.flipped

        # Ensure the enemy is on the platform
        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                on_platform = True
                break
        if not on_platform:
            self.rect.y += self.speed * self.direction

        # Check if the enemy is about to walk off the edge of a platform
        if self.direction == 1:  # Moving right
            if not any(platform.rect.collidepoint(self.rect.right + self.speed, self.rect.bottom) for platform in platforms):
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = not self.flipped
        elif self.direction == -1:  # Moving left
            if not any(platform.rect.collidepoint(self.rect.left - self.speed, self.rect.bottom) for platform in platforms):
                self.direction *= -1
                self.image = pygame.transform.flip(self.image, True, False)
                self.flipped = not self.flipped

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Coin:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - self.width), 500, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.running = False
        self.player = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 60)  # Adjusted player initial position
        platform_width = SCREEN_WIDTH // 2 - 50
        self.platform1 = Platform(0, SCREEN_HEIGHT - 10, platform_width, 10)
        self.platform2 = Platform(SCREEN_WIDTH - platform_width, SCREEN_HEIGHT - 10, platform_width, 10)
        self.coin = Coin()
        self.score = Score()
        self.start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, "Start", (128, 128, 128), self.start_game)
        self.restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, "Restart", (128, 128, 128), self.start_game)
        self.start_time = 0
        # Calculate the center position of the second platform
        enemy_x = self.platform2.rect.x + (self.platform2.rect.width // 2) - 20  # 20 is half the width of the enemy
        enemy_y = self.platform2.rect.y - 40  # 40 is the height of the enemy
        self.enemies = [Enemy(enemy_x, enemy_y, player_sprite.get_width(), player_sprite.get_height())]

    def start_game(self):
        self.running = True
        self.score.reset()
        self.start_time = pygame.time.get_ticks()
        self.player.rect.x = SCREEN_WIDTH // 4
        self.player.rect.y = SCREEN_HEIGHT - 60
        self.player.velocity_y = 0
        self.player.jumping = False

    def end_game(self):
        self.running = False
        self.display_end_screen()

    def display_end_screen(self):
        screen.fill(WHITE)
        final_score_text = self.score.font.render(f"Final Score: {self.score.score}", True, BLACK)
        high_score_text = self.score.font.render(f"High Score: {self.score.high_score}", True, BLACK)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        self.restart_button.draw(screen)
        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not self.running and self.start_button.is_clicked(pos):
                        self.start_button.action()
                    if not self.running and self.restart_button.is_clicked(pos):
                        self.restart_button.action()

            keys = pygame.key.get_pressed()
            if self.running:
                self.player.handle_movement(keys)
                self.player.apply_gravity([self.platform1, self.platform2])

                # Move enemies and check for collisions with platforms
                for enemy in self.enemies:
                    enemy.move([self.platform1, self.platform2])
                    # Add a buffer to the collision detection
                    if self.player.rect.colliderect(enemy.rect.inflate(-5, -5)):
                        self.end_game()

                # Check for coin collision
                self.player.grabcoin(self.coin, self.score)

                # Check for game over
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                if elapsed_time >= GAME_DURATION or self.player.rect.top > SCREEN_HEIGHT:
                    self.end_game()

                # Draw everything
                screen.fill(WHITE)
                self.coin.draw(screen)
                self.platform1.draw(screen)
                self.platform2.draw(screen)
                self.player.draw(screen)
                for enemy in self.enemies:
                    enemy.draw(screen)
                self.score.display(screen)

                # Display timer
                timer_text = self.score.font.render(f"Time: {int(GAME_DURATION - elapsed_time)}", True, BLACK)
                screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))

            else:
                screen.fill(WHITE)
                if self.score.score > 0:
                    self.restart_button.draw(screen)
                else:
                    self.start_button.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

game = Game()
game.run()