import pygame
import os
import csv
from Characters.player import Player
from Characters.Enemy import Enemy
from Ammo import Ammo
from Bandage import Bandage
from blocks import Block
from Door import Door
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
ROWS = 16
TILE_SIZE = SCREEN_HEIGHT // ROWS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (144, 201, 120)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Playable Level")

clock = pygame.time.Clock()

tile_images = []
TILE_TYPES = 14
for i in range(TILE_TYPES):
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_images.append(img)

block_images = []
for i in range(10):
    img = pygame.image.load(f'assets/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    block_images.append(img)

ammo_image_path = 'assets/10.png'
bandage_image_path = 'assets/11.png'

background = pygame.image.load("assets/single_background.png").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH + 300, SCREEN_HEIGHT + 100))
background_width = background.get_width()
background_height = background.get_height()

SCROLL_MULTIPLIER = 1.5

def load_level(level_file):
    world_data = []
    try:
        level_path = os.path.join("LVLS", level_file)
        with open(level_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                world_data.append([int(tile) for tile in row if tile.strip()])
    except FileNotFoundError:
        return None
    except ValueError:
        return None
    return world_data

def draw_level(world_data):
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < len(tile_images):
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE
                screen.blit(tile_images[tile], (tile_x, tile_y))

def pause_menu():
    paused = True
    font = pygame.font.Font(None, 50)
    while paused:
        screen.fill(BLACK)
        pause_text = font.render("Paused", True, WHITE)
        resume_text = font.render("Press R to Resume", True, WHITE)
        quit_text = font.render("Press Q to Return to Menu", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(pause_text, pause_rect)
        screen.blit(resume_text, resume_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                if event.key == pygame.K_q:
                    return "menu"

def death_menu(score):
    font = pygame.font.Font(None, 50)
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        death_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {score:.2f}%", True, WHITE)
        restart_text = font.render("Press R to Restart", True, WHITE)
        quit_text = font.render("Press Q to Quit to Menu", True, WHITE)
        death_rect = death_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(death_text, death_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "menu"

class Camera:
    def __init__(self, width, height, level_width):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.level_width = level_width

    def update(self, target_rect):
        self.offset_x = max(0, min(target_rect.centerx - self.width // 2, self.level_width - self.width))
        self.offset_y = 0

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)

def draw_background(camera, level_width):
    for x in range(0, max(level_width, SCREEN_WIDTH) + background_width, background_width):
        for y in range(0, SCREEN_HEIGHT + background_height, background_height):
            screen.blit(background, camera.apply(pygame.Rect(x, y, background_width, background_height)))

def draw_zombie_score(screen, score, position=(10, 10)):
    font = pygame.font.Font(None, 24)
    score_text = f"Zombies Killed: {score:.2f}%"
    text_surface = font.render(score_text, True, (255, 255, 255))
    screen.blit(text_surface, position)

def main(level_file):
    world_data = load_level(level_file)
    if not world_data:
        return
    level_width = len(world_data[0]) * TILE_SIZE if world_data else SCREEN_WIDTH
    level_height = len(world_data) * TILE_SIZE
    player_start_x, player_start_y = 100, 500
    enemies = []
    ammo_items = []
    bandages = []
    blocks = pygame.sprite.Group()
    door = None
    total_zombies = 0
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile <= 9:
                blocks.add(Block(x * TILE_SIZE, y * TILE_SIZE, block_images[tile]))
            elif tile == 12:
                player_start_x, player_start_y = x * TILE_SIZE, y * TILE_SIZE
            elif tile == 13:
                enemies.append(Enemy(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE, None))
                total_zombies += 1
            elif tile == 10:
                ammo_items.append(Ammo(x * TILE_SIZE, y * TILE_SIZE, "assets/10.png", TILE_SIZE))
            elif tile == 11:
                bandages.append(Bandage(x * TILE_SIZE, y * TILE_SIZE, "assets/11.png", TILE_SIZE))
            elif tile == 14:
                door = Door(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, "assets/14.png")
    player = Player(x=player_start_x, y=player_start_y, player_sprite=None, screen_width=SCREEN_WIDTH)
    player.speed = 2
    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, level_width)
    running = True
    score = 0
    while running:
        screen.fill(GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    action = pause_menu()
                    if action == "menu":
                        return
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        if keys[pygame.K_LEFT]:
            if player.rect.left > 0:
                player.rect.x -= player.speed
        if keys[pygame.K_RIGHT]:
            if player.rect.right < level_width:
                player.rect.x += player.speed
        camera.update(player.rect)
        player.handle_input(keys, mouse_buttons)
        player.apply_gravity(blocks)
        player.update()
        player.update_bullets()
        for bullet in player.bullets[:]:
            for enemy in enemies[:]:
                if bullet.check_collision(enemy.mask, enemy.rect):
                    enemy.take_damage(20)
                    player.bullets.remove(bullet)
                    break
        for block in blocks:
            if block.check_collision(player.mask, player.rect):
                if player.velocity_y > 0:
                    player.rect.bottom = block.rect.top
                    player.velocity_y = 0
                    player.jumping = False
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                offset_x = enemy.rect.x - player.rect.x
                offset_y = enemy.rect.y - player.rect.y
                if player.mask.overlap(enemy.mask, (offset_x, offset_y)):
                    player.take_damage(10, enemy.rect)
        for enemy in enemies[:]:
            if enemy.is_dead and enemy.death_animation_done:
                enemies.remove(enemy)
                continue
            enemy.move_toward_player(player, blocks)
            enemy.animate()
        zombies_killed = total_zombies - len(enemies)
        score = (zombies_killed / total_zombies) * 100 if total_zombies > 0 else 0
        for bullet in player.bullets[:]:
            for block in blocks:
                if bullet.check_collision(block.mask, block.rect):
                    player.bullets.remove(bullet)
                    break
        for ammo in ammo_items[:]:
            ammo.check_collision(player)
            if ammo.collected:
                ammo_items.remove(ammo)
        for bandage in bandages[:]:
            bandage.check_collision(player)
            if bandage.collected:
                bandages.remove(bandage)
        if door and door.check_collision(player.mask, player.rect):
            current_level_index = int(level_file.replace("level", "").replace("_data.csv", ""))
            next_level = f"level{current_level_index + 1}_data.csv"
            action = door.handle_level_end(screen, score, next_level=next_level if os.path.exists(f"LVLS/{next_level}") else None)
            if action == "next":
                main(next_level)
                return
            elif action == "menu":
                return
        if player.health <= 0:
            if not player.death_animation_done:
                player.play_death_animation()
                player.animate()
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
                screen.blit(player.image, camera.apply(player.rect))
                player.draw_ammo_count(screen)
                player.draw_health_bar(screen)
                player.draw_score(screen, score, position=(10, 50))
                draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))
                pygame.display.flip()
                clock.tick(60)
                continue
            for _ in range(60):
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
                screen.blit(player.image, camera.apply(player.rect))
                player.draw_ammo_count(screen)
                player.draw_health_bar(screen)
                player.draw_score(screen, score, position=(10, 50))
                draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))
                pygame.display.flip()
                clock.tick(60)
            action = death_menu(score)
            if action == "restart":
                main(level_file)
                return
            elif action == "menu":
                return
        if player.rect.top > SCREEN_HEIGHT:
            action = death_menu(score)
            if action == "restart":
                main(level_file)
                return
            elif action == "menu":
                return
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
        screen.blit(player.image, camera.apply(player.rect))
        player.draw_ammo_count(screen)
        player.draw_health_bar(screen)
        player.draw_score(screen, score, position=(10, 50))
        draw_zombie_score(screen, score, position=(SCREEN_WIDTH - 175, 10))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main("level0_data.csv")