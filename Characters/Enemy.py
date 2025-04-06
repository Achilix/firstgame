import pygame  # Import pygame

class Enemy:
    def __init__(self, x, y, width, height, enemy_sprite):
        # Load the walk animation sprite sheet
        self.sprite_sheet_walk = pygame.image.load('SPRITES/Enemy/Walk.png').convert_alpha()
        self.frames_walk = self.load_frames(self.sprite_sheet_walk, num_frames=10)  # 10 frames for walking

        # Load the death animation sprite sheet
        self.sprite_sheet_dead = pygame.image.load('SPRITES/Enemy/Dead.png').convert_alpha()
        self.frames_dead = self.load_frames(self.sprite_sheet_dead, num_frames=5)  # 5 frames for death animation

        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust animation speed
        self.image = self.frames_walk[self.current_frame]  # Start with the first walk frame
        self.rect = self.image.get_rect(topleft=(x, y))  # Set the initial position

        # Adjust the y position to ensure the enemy is on the ground
        self.rect.y = y - (self.rect.height - height)

        self.speed = 1  # Reduced speed to make the zombie slower
        self.flipped = False
        self.health = 100  # Zombie's health (out of 100)
        self.is_dead = False  # Track if the enemy is dead
        self.death_animation_done = False  # Track if the death animation is complete

        # Create a mask for precise collision detection
        self.mask = pygame.mask.from_surface(self.image)

        self.velocity_y = 0  # Vertical velocity for gravity
        self.gravity = 0.5  # Gravity strength

    def load_frames(self, sprite_sheet, num_frames):
        """
        Split the sprite sheet into individual frames and scale them to 1.5 times their size.
        :param sprite_sheet: The loaded sprite sheet.
        :param num_frames: The total number of frames in the sprite sheet.
        :return: A list of frames.
        """
        frames = []
        frame_width = sprite_sheet.get_width() // num_frames  # Calculate the width of each frame
        frame_height = sprite_sheet.get_height()  # Use the full height of the sprite sheet

        for i in range(num_frames):
            # Extract each frame
            frame = sprite_sheet.subsurface(pygame.Rect(
                i * frame_width,  # Start at the correct x-coordinate for each frame
                0,  # Start at the top of the sprite sheet
                frame_width,  # Width of the frame
                frame_height  # Height of the frame
            ))
            # Scale the frame to 1.5 times its size
            frame = pygame.transform.scale(frame, (int(frame_width * 1.5), int(frame_height * 1.5)))
            frames.append(frame)

        return frames

    def animate(self):
        if self.is_dead:
            # Play death animation
            if not self.death_animation_done:
                self.current_frame += self.animation_speed
                if self.current_frame >= len(self.frames_dead):
                    self.current_frame = len(self.frames_dead) - 1
                    self.death_animation_done = True  # Mark the death animation as complete
                self.image = self.frames_dead[int(self.current_frame)]
        else:
            # Play walk animation
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames_walk):
                self.current_frame = 0
            self.image = self.frames_walk[int(self.current_frame)]

        # Flip the image if necessary
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

        # Update the mask and rect whenever the image changes
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)  # Keep the enemy's position consistent

    def apply_gravity(self, blocks):
        """
        Apply gravity to the enemy and ensure it falls when there is no block beneath it.
        :param blocks: A list or group of block objects.
        """
        self.velocity_y += self.gravity  # Increase velocity due to gravity
        self.rect.y += self.velocity_y  # Move the enemy vertically

        # Check for collisions with blocks
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velocity_y > 0:  # Falling down
                    self.rect.bottom = block.rect.top  # Stop at the top of the block
                    self.velocity_y = 0  # Reset vertical velocity

    def move_toward_player(self, player, blocks):
        """
        Move the enemy horizontally toward the player if the player is within line of sight.
        Allow the enemy to fall into holes.
        :param player: The player object.
        :param blocks: A list or group of block objects.
        """
        if not self.is_dead:  # Only move if the enemy is alive
            # Apply gravity before moving
            self.apply_gravity(blocks)

            # Check if the player is within line of sight
            player_in_sight = abs(self.rect.x - player.rect.x) < 300 and abs(self.rect.y - player.rect.y) < 50

            if player_in_sight:
                # Move toward the player
                if self.rect.x < player.rect.x:
                    self.flipped = False  # Face right
                    self.rect.x += self.speed  # Move right
                elif self.rect.x > player.rect.x:
                    self.flipped = True  # Face left
                    self.rect.x -= self.speed  # Move left
            else:
                # Patrol behavior: Move right to left
                if not hasattr(self, "patrol_direction"):
                    self.patrol_direction = 1  # 1 for right, -1 for left
                    self.patrol_start_x = self.rect.x  # Save the starting position
                    self.patrol_range = 100  # Patrol range in pixels

                # Move in the current patrol direction
                self.rect.x += self.speed * self.patrol_direction

                # Reverse direction if the enemy reaches the patrol range
                if self.rect.x > self.patrol_start_x + self.patrol_range:
                    self.patrol_direction = -1  # Switch to moving left
                    self.flipped = True  # Face left
                elif self.rect.x < self.patrol_start_x:
                    self.patrol_direction = 1  # Switch to moving right
                    self.flipped = False  # Face right

            # Check for collisions with blocks
            for block in blocks:
                if self.rect.colliderect(block.rect):
                    # Adjust position to prevent walking through the block
                    if self.rect.x < block.rect.x:  # Moving right
                        self.rect.right = block.rect.left
                        self.patrol_direction = -1  # Reverse patrol direction
                    elif self.rect.x > block.rect.x:  # Moving left
                        self.rect.left = block.rect.right
                        self.patrol_direction = 1  # Reverse patrol direction

    def take_damage(self, amount):
        if self.is_dead:
            return
        self.health -= amount
        print(f"Enemy health: {self.health}")  # Debugging print
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            print("Enemy is dead!")  # Debugging print

    def draw(self, screen, camera):
        """
        Draw the enemy and its health bar using the camera offset.
        """
        screen.blit(self.image, camera.apply(self.rect))

        if not self.is_dead:   
            # Draw the health bar
            # Red background (full health bar)
            health_bar_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width, 5)
            screen.blit(pygame.Surface((health_bar_rect.width, health_bar_rect.height)), camera.apply(health_bar_rect))
            # Green foreground (current health)
            current_health_rect = pygame.Rect(self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5)
            screen.blit(pygame.Surface((current_health_rect.width, current_health_rect.height)), camera.apply(current_health_rect))