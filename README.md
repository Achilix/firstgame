# Pygame Game: "Zombie Survival"

## Description
A Pygame-based game where the player must survive against zombies while navigating the environment. The game includes player movement, enemy AI, health mechanics, shooting mechanics, and custom level creation. The goal is to survive as long as possible while managing limited resources and avoiding enemies.

---

## Current Features (Progress: **100% Complete**)

### Main Menu
- **Title**: Displays the game title "Zombie Survival" at the top of the menu.
- **Start Game**: A button to start the game and select levels.
- **Level Builder**: A button to launch the level builder for creating custom levels.
- **Quit**: A button to exit the game.

### Level Selection Menu
- **Dynamic Level Loading**: Automatically loads levels from the `LVLS` directory.
- **Back Button**: Allows the player to return to the main menu.

### Player
- **Movement**: The player can move left, right, and jump.
- **Health**: The player has health that decreases when colliding with enemies.
- **Collision Detection**: The player interacts with platforms and enemies using **mask-based collision detection**.
- **Health Bar**: A health bar is displayed above the player.
- **Shooting**: The player can shoot bullets, which interact with enemies and blocks using **mask-based collision detection**.

### Enemy
- **Chasing Behavior**: Enemies move toward the player horizontally.
- **Health**: Enemies have health and can take damage.
- **Health Bar**: A health bar is displayed above each enemy.
- **Damage**: Enemies can be damaged by bullets or other attacks using **mask-based collision detection**.

### Bullets
- **Shooting Mechanics**: Bullets are fired by the player and interact with enemies and blocks.
- **Mask-Based Collision**: Bullets use pixel-perfect collision detection for interactions.

### Game Mechanics
- **Scrolling Background**: A dynamic background scrolls with the player's movement.
- **Restart Button**: A button to restart the game after the player dies.
- **Basic Level Design**: A level builder is included for creating custom levels.
- **Dynamic Scrolling**: The screen scrolls as the player moves, with adjustable scroll speed.

### Level Builder
- **Custom Level Creation**: Allows users to create and save custom levels.
- **Tile-Based Editing**: Users can place tiles, enemies, and items on a grid.
- **Save and Load**: Levels are saved as CSV files and can be loaded dynamically in the game.

### Visual and Audio Enhancements
- **Custom Font**: The game uses the retro-style `PressStart2P` font for menus and titles.
- **Background Music**: Background music enhances the gameplay experience.
- **Sound Effects**: Includes sound effects for movement, attacks, and collisions.

---

## How to Run the Game
1. Install Python and Pygame.
2. Clone this repository.
3. Run `menu.py` to start the game.
4. Use the main menu to:
   - Start the game and select a level.
   - Launch the level builder to create custom levels.
   - Quit the game.
5. Use the arrow keys to move the player and avoid enemies.
6. Use the mouse to shoot bullets.

---

## Future Improvements
- **Advanced Enemy Behavior**: Add different types of enemies with unique behaviors.
- **Vertical Movement**: Allow enemies to jump or climb platforms.
- **Scoring System**: Track and display the player's score and high scores.
- **Dynamic Difficulty**: Adjust the difficulty based on the player's performance.
- **Animations**: Add animations for the player, enemies, and attacks.

---

## Completion Status
- **Current Progress**: **100%**
- **Remaining Tasks**: None (all planned features implemented).

---

Let me know if you need further updates or adjustments!