# Level Builder and Simple Platform Game

This project contains a level builder for a platform game using Pygame, as well as a simple platform game where the player needs to collect coins within a time limit.

## Features

### Level Builder
- Create and edit levels by placing tiles on a grid.
- Save and load level data to/from CSV files.
- Scroll the background to create larger levels.
- Choose from different tile types to place on the grid.

### Simple Platform Game
- Control a player character to collect coins.
- Avoid enemies and navigate platforms.
- Score tracking and high score display.
- Game duration of 30 seconds.

## Installation

1. Make sure you have Python and Pygame installed. You can install Pygame using pip:

    ```sh
    pip install pygame
    ```

2. Clone this repository or download the source code.

3. Place the assets (images) in the `assets` directory.

## Usage

### Level Builder

1. Run the `lvlbuilder.py` script to start the level builder:

    ```sh
    python lvlbuilder.py
    ```

2. Use the mouse to place tiles on the grid:
    - Left-click to place the selected tile.
    - Right-click to remove a tile.

3. Use the following keys to control the level builder:
    - `UP` arrow: Increase the level number.
    - `DOWN` arrow: Decrease the level number.
    - `LEFT` arrow: Scroll the background to the left.
    - `RIGHT` arrow: Scroll the background to the right.
    - `Right Shift`: Increase the scroll speed.
    - `Left Shift`: Decrease the scroll speed.

4. Click the "Save" button to save the level data to a CSV file.
5. Click the "Load" button to load the level data from a CSV file.

### Simple Platform Game

1. Run the `app.py` script to start the game:

    ```sh
    python app.py
    ```

2. Use the arrow keys to move the player:
    - `LEFT` arrow: Move left.
    - `RIGHT` arrow: Move right.
    - `SPACE`: Jump.

3. Collect coins to increase your score and avoid enemies.

4. The game lasts for 30 seconds. Try to collect as many coins as possible within the time limit.

## File Structure

- `lvlbuilder.py`: Main script for the level builder.
- `button.py`: Contains the `Button` class used for creating buttons.
- `app.py`: Main script for the simple platform game.
- `level0_data.csv`: Example level data file.
- `assets/`: Directory containing the images used for tiles and buttons.

## License

This project is licensed under the MIT License.
