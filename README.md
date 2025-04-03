# Pygame Game: Zombie Survival

## Description
A Pygame-based game where the player must survive against zombies while navigating the environment. The game includes player movement, enemy AI, health mechanics, and basic interactions. The goal is to survive as long as possible while managing limited resources and avoiding enemies.

---

## Current Features (Progress: **85% Complete**)

### Player
- **Movement**: The player can move left, right, and jump.
- **Health**: The player has health that decreases when colliding with enemies.
- **Knockback**: The player experiences knockback when hit by an enemy.
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
- **Restart Button**: A button to restart the game after the player dies.
- **Basic Level Design**: A level builder is included for creating custom levels.

---

## Features Still Needed (Remaining: **15%**)

### Advanced Enemy Behavior
- **Enemy Types**: Add different types of enemies with unique behaviors.
- **Vertical Movement**: Allow enemies to jump or climb platforms.

### Scoring System
- **Score Display**: Show the player's score on the screen.
- **High Score**: Track and display the highest score.

### Difficulty Manager
- **Dynamic Difficulty**: Adjust the difficulty based on the player's performance:
  - Spawn more zombies if the player is doing well.
  - Reduce ammo pickups or increase enemy speed as the game progresses.
  - Add stronger enemies or bosses at higher difficulty levels.

### Visual and Audio Enhancements
- **Animations**: Add animations for the player, enemies, and attacks.
- **Sound Effects**: Add sound effects for movement, attacks, and collisions.
- **Background Music**: Include background music for a more immersive experience.

---

## Percentage of Completion
- **Current Progress**: **85%**
- **Remaining Tasks**: **15%**

---

## How to Run the Game
1. Install Python and Pygame.
2. Clone this repository.
3. Run `test.py` to start the game.
4. Use the arrow keys to move the player and avoid enemies.
5. Use the mouse to shoot bullets.

---

Let me know if you need further updates or adjustments!