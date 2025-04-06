class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.min_x = 0  # Minimum camera offset
        self.max_x = 672  # Maximum camera offset

    def update(self, target_rect):
        # Move the camera only when the player reaches 3/4 of the screen width
        threshold_left = self.width // 4  # Left threshold
        threshold_right = self.width // 4 * 3  # Right threshold

        if target_rect.centerx < self.offset_x + threshold_left:
            self.offset_x = max(self.min_x, target_rect.centerx - threshold_left)
        elif target_rect.centerx > self.offset_x + threshold_right:
            self.offset_x = min(self.max_x, target_rect.centerx - threshold_right)

        # Keep the vertical offset fixed
        self.offset_y = 0

    def apply(self, rect):
        # Apply the camera offset to the given rectangle
        return rect.move(-self.offset_x, -self.offset_y)
