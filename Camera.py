class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.min_x = 0
        self.max_x = 672

    def update(self, target_rect):
        threshold_left = self.width // 4
        threshold_right = self.width // 4 * 3
        if target_rect.centerx < self.offset_x + threshold_left:
            self.offset_x = max(self.min_x, target_rect.centerx - threshold_left)
        elif target_rect.centerx > self.offset_x + threshold_right:
            self.offset_x = min(self.max_x, target_rect.centerx - threshold_right)
        self.offset_y = 0

    def apply(self, rect):
        return rect.move(-self.offset_x, -self.offset_y)
