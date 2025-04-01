import pygame  # Import pygame

class Enemy:
    def load_frames(self, sprite_sheet, num_frames):
        """
        Split the sprite sheet into individual frames.
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
            # Scale the frame to a larger size (e.g., 100x100)
            frame = pygame.transform.scale(frame, (100, 100))  # Adjust size as needed
            frames.append(frame)

        return frames

    def __init__(self, x, y, width, height, enemy_sprite):
        # Load the walk animation sprite sheet
        self.sprite_sheet_walk = pygame.image.load('SPRITES/Enemy/Walk.png').convert_alpha()
        self.frames_walk = self.load_frames(self.sprite_sheet_walk, num_frames=10)  # 10 frames for walking

        self.current_frame = 0
        self.animation_speed = 0.2  # Adjust animation speed
        self.image = self.frames_walk[self.current_frame]  # Start with the first walk frame
        self.rect = self.image.get_rect(topleft=(x, y - 50))  # Adjust y position to lift the zombie above the ground

        self.speed = 1  # Reduced speed to make the zombie slower
        self.flipped = False
        self.health = 100  # Zombie's health (out of 100)

    def animate(self):
        """
        Handle the enemy's walk animation.
        """
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames_walk):
            self.current_frame = 0
        self.image = self.frames_walk[int(self.current_frame)]

        # Flip the image if the enemy is facing left
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)

    def move_toward_player(self, player):
        """
        Move the enemy toward the player's position horizontally.
        Stop moving if colliding with the player.
        :param player: The player object to chase.
        """
        # Check for collision with the player
        if self.rect.colliderect(player.rect):
            return  # Stop moving if colliding with the player

        # Move horizontally toward the player
        if self.rect.centerx < player.rect.centerx:
            self.rect.x += self.speed  # Move right
            if self.flipped:  # Flip the image to face right
                self.flipped = False
        elif self.rect.centerx > player.rect.centerx:
            self.rect.x -= self.speed  # Move left
            if not self.flipped:  # Flip the image to face left
                self.flipped = True

        # Animate the enemy while moving
        self.animate()

    def take_damage(self, amount):
        """
        Reduce the enemy's health by the specified amount.
        :param amount: The amount of damage to reduce from the enemy's health.
        """
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Enemy is dead!")

    def draw(self, screen):
        """
        Draw the enemy and its health bar.
        """
        # Draw the enemy sprite
        screen.blit(self.image, self.rect.topleft)

        # Draw the health bar
        # Red background (full health bar)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
        # Green foreground (current health)
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * (self.health / 100), 5))