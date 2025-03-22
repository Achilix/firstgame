class GunPickup:
    def __init__(self, x, y, gun):
        """
        Initialize the GunPickup object.
        :param x: The x-coordinate of the gun on the map.
        :param y: The y-coordinate of the gun on the map.
        :param gun: The gun object (e.g., Rifle or Pistol).
        """
        self.gun = gun
        self.rect = self.gun.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        """
        Draw the gun on the map.
        """
        screen.blit(self.gun.image, self.rect.topleft)