import pygame
import button
import csv
import os  # Import os to handle file paths

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Builder')
#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
TITLE_TYPES = 15  # Updated to match the available images
current_tile = 0
level = 0
font = pygame.font.SysFont('Futura', 30)
#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (255, 25, 25)
#empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#function for text on screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Load and scale images
SKY = pygame.image.load('assets\single_background.png').convert_alpha()
SKY = pygame.transform.scale(SKY, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
#store titles
img_list = []
for x in range(TITLE_TYPES):
    img = pygame.image.load(f'assets/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('assets/save_btn.png').convert_alpha()
load_img = pygame.image.load('assets/load_btn.png').convert_alpha()

def draw_bg():
    screen.fill(GREEN)
    width = SKY.get_width()
    for x in range(5):
         screen.blit(SKY, ((x* width) -scroll, 0))

#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT)) 
    #horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH + SIDE_MARGIN, c * TILE_SIZE))

#function to draw world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if 0 <= tile < len(img_list):  # Ensure the tile index is valid
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))
            elif tile != -1:  # Debug invalid tile values
                print(f"Invalid tile value: {tile} at position ({x}, {y})")

#create buttons
# Create buttons using images
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

#make button list 
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 50 + 75 * button_row, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_col = 0
        button_row += 1

# Ensure the LVLS folder exists
if not os.path.exists("LVLS"):
    os.makedirs("LVLS")

def load_level(level):
    world_data = []
    try:
        with open(f'LVLS/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # Ensure all tile values are valid
                world_data.append([tile if 0 <= tile < len(img_list) else -1 for tile in map(int, row)])
    except FileNotFoundError:
        print(f"Error: Level {level} does not exist.")
        return None
    return world_data

run = True
while run:
    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level:{level}', font, WHITE, 50, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 50, SCREEN_HEIGHT + LOWER_MARGIN - 50)
    # Save level data
    if save_button.draw(screen):
        with open(f'LVLS/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
        print(f"Level {level} saved to LVLS/level{level}_data.csv")

    # Load level data
    if load_button.draw(screen):
        # Reset scroll back to the start of the level
        scroll = 0
        loaded_data = load_level(level)
        if loaded_data is not None:
            world_data = loaded_data
            print(f"Level {level} loaded from LVLS/level{level}_data.csv")
    #draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    #choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    #highlight the selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #scroll the background
    max_scroll = SKY.get_width() * 5 - SCREEN_WIDTH
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < max_scroll:
        scroll += 5 * scroll_speed

    #add new tiles to the screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE
    #check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:  # Left click to place a tile
            if 0 <= current_tile < len(img_list) and world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:  # Right click to remove a tile
            world_data[y][x] = -1
    #reset level   
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
                # Reset scroll back to the start of the level
                scroll = 0
                loaded_data = load_level(level)
                if loaded_data is not None:
                    world_data = loaded_data
                    print(f"Level {level} loaded from LVLS/level{level}_data.csv")
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
                # Reset scroll back to the start of the level
                scroll = 0
                loaded_data = load_level(level)
                if loaded_data is not None:
                    world_data = loaded_data
                    print(f"Level {level} loaded from LVLS/level{level}_data.csv")
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed += 1
            if event.key == pygame.K_LSHIFT:
                scroll_speed -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False

pygame.quit()