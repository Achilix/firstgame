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
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jumping = False
        self.jump_height = 10

    def handle_movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.velocity_y = -self.jump_height

    def apply_gravity(self, platform):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Collision with the platform
        if self.rect.bottom >= platform.rect.top:
            self.rect.bottom = platform.rect.top
            self.velocity_y = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

    def grabcoin(self, coin, score):
        if self.rect.colliderect(coin.rect):
            score.update()
            print("Coin collected")
            coin.rect.x = random.randint(0, SCREEN_WIDTH - coin.width)
            coin.rect.y = 500
            return True
        return False

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Coin:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - self.width),500, self.width, self.height)

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
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.platform = Platform(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)
        self.coin = Coin()
        self.score = Score()
        self.start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, "Start", (128, 128, 128), self.start_game)
        self.restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, "Restart", (128, 128, 128), self.start_game)
        self.start_time = 0

    def start_game(self):
        self.running = True
        self.score.reset()
        self.start_time = pygame.time.get_ticks()

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
                self.player.apply_gravity(self.platform)

                # Check for coin collision
                self.player.grabcoin(self.coin, self.score)

                # Check for game over
                elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
                if elapsed_time >= GAME_DURATION:
                    self.end_game()

                # Draw everything
                screen.fill(WHITE)
                self.coin.draw(screen)
                self.platform.draw(screen)
                self.player.draw(screen)
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

# Run the game
game = Game()
game.run()